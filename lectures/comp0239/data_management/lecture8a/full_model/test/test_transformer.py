from .fixtures.ord import small, folder, repeated_input, both_sides
from ..transformer import file_to_model, files_to_model
from ..transformer import reactants, products, collapse_smiles, reaction_to_structure
from ..transformer import ORD_to_structure, structure_to_UID, ORD_to_SQLAlchemy
from .fixtures.lite import sqlite
from pysmiles import read_smiles
from ..model import create_tables, session, add_items, Molecule

import os, logging
logging.getLogger('pysmiles').setLevel(logging.ERROR)  
from rdkit import RDLogger

RDLogger.DisableLog('rdApp.*')  

def test_can_parse_ord():
    small_model = file_to_model(small)
    assert len(small_model) == 750

def test_can_parse_ord_folder():

    model = files_to_model(os.path.join(folder,'01',"*"))
    assert len(list(model)) == 4117

def test_can_parse_nested_folder():
    model = files_to_model(os.path.join(folder,"**","*"))
    assert len(list(model)) == 4117 + 750

def test_can_get_reactant():
    small_model = file_to_model(small)
    r1 = small_model[0]
    reac = next(reactants(r1, False))
    assert reac.nodes[0]['element'] == 'C'

def test_can_get_reactants():
    small_model = file_to_model(small)
    r1 = small_model[0]
    reacs = list(reactants(r1, False))

def test_can_get_product():
    small_model = file_to_model(small)
    r1 = small_model[0]
    prod = next(products(r1, False))
    assert prod.nodes[0]['element'] == 'C'

def test_collapse_smiles():
    smiles = read_smiles("CCOC1=C(C=C2C(=C1)N=CC(=C2NC3=C(C=C(C=C3)F)F)C(=O)OCC)N4CCN(CC4)C(C)C")
    collapsed = collapse_smiles(smiles)
    assert collapsed['C'] == 27
    assert collapsed['H'] == 32
    assert collapsed['N'] == 4

def test_structure_to_UID():
    smiles = read_smiles("CCOC1=C(C=C2C(=C1)N=CC(=C2NC3=C(C=C(C=C3)F)F)C(=O)OCC)N4CCN(CC4)C(C)C")
    collapsed = collapse_smiles(smiles)
    assert structure_to_UID(collapsed) == "H32C27O3N4F2"

def test_reaction_structure():
    small_model = file_to_model(small)
    r1 = small_model[0]
    reaction = reaction_to_structure(r1)
    assert reaction['reactants'][0]['C'] == 1

def test_ORD_structure():
    small_model = file_to_model(small)
    reactions = ORD_to_structure(small_model)
    assert reactions[0]['reactants'][0]['C'] == 1

def test_map_ORD_to_SQLAlchemy_local():
    small_model = file_to_model(small)
    items = ORD_to_SQLAlchemy(small_model)

def test_map_ORD_to_SQLAlchemy():
    small_model = file_to_model(small)
    items = ORD_to_SQLAlchemy(small_model)
    with sqlite() as db:
        create_tables(db)
        s = session(db)
        add_items(items,s) #with dedup
        s.commit()

        mol = s.get(Molecule,'H32C27O3N4F2')
        assert mol
        assert mol.elements[0].symbol == 'H'
        assert mol.elements[0].number == 32

def test_repeated_input_ORD_to_SQLAlchemy():
    items = ORD_to_SQLAlchemy([repeated_input])
    with sqlite() as db:
        create_tables(db)
        s = session(db)
        add_items(items,s)
        s.commit()

def test_both_sides_ORD_to_SQLAlchemy():
    items = ORD_to_SQLAlchemy([both_sides])
    with sqlite() as db:
        create_tables(db)
        s = session(db)
        add_items(items,s)
        s.commit()