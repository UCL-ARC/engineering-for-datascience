from .fixtures.lite import sqlite
from .fixtures.tiny_db import tiny_db

from ..model import create_tables, drop_tables, session, add_items, Molecule, Reaction

from sqlalchemy import select
from sqlalchemy.exc import IntegrityError

def test_create_tables():
    with sqlite() as db:
        create_tables(db)

def test_model():
    with sqlite() as db:
        create_tables(db)
        s = session(db)
        add_items(tiny_db(), s)
        s.commit()
        mols = s.scalars(select(Molecule).where(Molecule.name == 'water')).all()
        assert len(mols)==1
        mol = mols[0]
        assert len(mol.elements) == 2
        assert mol.elements[0].symbol == "O"
        assert mol.elements[1].number == 2
        assert mol.elements[1].symbol == "H"
        reactions = s.scalars(select(Reaction)).all()
        assert len(reactions)==2
        reaction_2=reactions[1]
        assert reaction_2.molecules[2].name == 'water'
        reaction_1=reactions[0]
        assert reaction_1.molecules[2].name == 'water'

def test_model_duplicated():
    with sqlite() as db:
        create_tables(db)
        s = session(db)
        add_items(tiny_db()+tiny_db(), s)
        s.commit()
        mols = s.scalars(select(Molecule).where(Molecule.name == 'water')).all()
        assert len(mols)==1
        mol = mols[0]
        assert len(mol.elements) == 2
        assert mol.elements[0].symbol == "O"
        assert mol.elements[1].number == 2
        assert mol.elements[1].symbol == "H"
        reactions = s.scalars(select(Reaction)).all()
        assert len(reactions)==4 # Duplicate **reactions** are allowed
        assert reactions[0].molecules[2].name == 'water'
        assert reactions[1].molecules[2].name == 'water'
        assert reactions[2].molecules[2].name == 'water'
        assert reactions[3].molecules[2].name == 'water'
        # But they all contain the same water molecule

