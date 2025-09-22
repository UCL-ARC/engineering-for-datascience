from ord_schema import message_helpers, validations
from ord_schema.proto.dataset_pb2 import Dataset
from ord_schema.proto.reaction_pb2 import CompoundIdentifier
from pysmiles import read_smiles
from .model import Element, Molecule, Reaction, Participant, AtomsPerMolecule, add_item

from functools import reduce
from itertools import chain
from glob import glob

import pandas as pd

import logging
logger = logging.getLogger('ETL')

from google.protobuf import text_format

def files_to_model(path):
    # Given path is a path to a message, or a glob to be globbed for messages.
    # Should recursive
    logger.debug(f"Path to data {path}")
    files = glob(path)
    logger.info(f"Found {len(files)} files to parse")
    logger.debug(f"Files to parse: \n {files}")
    result= reduce(lambda x, y: x+y, map(file_to_model, files))
    logger.info(f"Found {len(result)} reactions to process.")
    return result

def file_to_model(path):
    data = message_helpers.load_message(path, Dataset)
    validations.validate_message(data)
    return list(data.reactions)

smiles_like = [CompoundIdentifier.SMILES, CompoundIdentifier.CXSMILES]

def reactants(reaction, collapse = True):
    # Pull out a table of reactants
    # Each reactant will be a smiles model of the molecule
    # This is wrong as it shows catalysts as reactants, but we're not here for science
    for input in reaction.inputs.values():
        for component in input.components:
            try:
                smiles = [id.value for id in component.identifiers if id.type in smiles_like ][0]
            except IndexError:
                logger.debug("Encountered molecule with no SMILES, skipping")
                continue
            graph = read_smiles(smiles)
            uid = structure_to_UID(collapse_smiles(graph))
            yield collapse_smiles(graph) if collapse else graph

def products(reaction, collapse = True):
    # Pull out a table of products and their stoichiometries
    # Each product will be a smiles model of the molecule
    for outcome in reaction.outcomes:
        for product in outcome.products:
            try:
                smiles = [id.value for id in product.identifiers if id.type in smiles_like ][0]
            except IndexError:
                logger.debug("Encountered molecule with no SMILES, skipping")
                continue
            graph = read_smiles(smiles)
            uid = structure_to_UID(collapse_smiles(graph))
            yield collapse_smiles(graph) if collapse else graph


def collapse_smiles(smiles):
    # Turn a smiles object into just a count of atoms in the molecule
    result = {'H':0}
    for node in smiles.nodes.values():
        if node['element'] in result:
            result[node['element']] += 1
        else:
            result[node['element']] = 1
        result['H'] += node['hcount']
    
    return result

def reaction_to_structure(reaction):
    return {
        'reactants' : list(reactants(reaction)),
        'products' : list(products(reaction))
    }

def ORD_to_structure(model):
    return [reaction_to_structure(reaction) for reaction in model]

def structure_to_UID(molecule):
    return "".join([f"{element}{number}" for (element,number) in molecule.items()])


def ORD_to_SQLAlchemy(model, session=False):
    reactions = []
    reactions_count = len(model)
    for (n, reaction_m) in enumerate(model):

            logger.info(f"Transforming reaction {n}/{reactions_count}")
            reaction = Reaction()
            reactions.append(reaction)
            partipant_ids = set() # Ensure a given participant only occurs once in a given reaction
            for reactant in reactants(reaction_m):
                uid = structure_to_UID(reactant)
                if uid in partipant_ids: 
                    logger.debug(f"Encountered repeated participant {uid}, skipping")
                    continue
                partipant_ids.add(uid)
                molecule = Molecule(name = uid)
                for (atom, count) in reactant.items():
                    molecule.add_atom(count, atom)
                reaction.add_participant(-1, molecule)

            for product in products(reaction_m):
                uid = structure_to_UID(product)
                if uid in partipant_ids: 
                    logger.debug(f"Encountered repeated participant {uid}, skipping")
                    continue
                partipant_ids.add(uid)
                molecule = Molecule(name = uid)
                for (atom, count) in product.items():
                    molecule.add_atom(count, atom)
                reaction.add_participant(1, molecule)

            if session:
                logger.debug("Saving reaction")
                try:
                    add_item(reaction,session)
                except:
                    # save the offending reaction for a new unit test
                    logger.error(type(reaction_m))
                    logger.error("Could not save reaction")
                    logger.error(text_format.MessageToString(reaction_m))
                    with open('failure.pb','w') as f:
                        f.write(text_format.MessageToString(reaction_m))
                    raise

    return reactions