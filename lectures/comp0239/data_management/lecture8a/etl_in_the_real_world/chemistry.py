"""
This file describes the data model which we will use.
It uses SQLAlchemy ORM to define the database tables.
"""

from sqlalchemy import Column, Integer, String, ForeignKey, create_engine
from sqlalchemy.orm import relationship, declarative_base, sessionmaker, mapped_column, Mapped
from typing import List
import os

Base = declarative_base()

import logging
logger = logging.getLogger('ETL')


class AtomsPerMolecule(Base):
    __tablename__ = "_atoms_per_molecule_"
    symbol: Mapped[str] = mapped_column(ForeignKey("elements.symbol"), primary_key=True)
    name: Mapped[str] = mapped_column(ForeignKey("molecules.name"), primary_key=True)
    number: Mapped[int]
    molecule: Mapped["Molecule"] = relationship(back_populates="elements")
    element: Mapped["Element"] = relationship(back_populates="molecules")

class Element(Base):
    __tablename__ = "elements"
    symbol: Mapped[str] = mapped_column(primary_key=True)
    molecules: Mapped[List["AtomsPerMolecule"]] = relationship(back_populates="element")

elements = {}

def element_factory(symbol):
    if not symbol in elements:
        elements[symbol] = Element(symbol = symbol)
    return elements[symbol]


class Participant(Base):
    __tablename__ = "participant"
    reaction_id: Mapped[int] = mapped_column(ForeignKey("reactions.id"), primary_key=True)
    name: Mapped[str] = mapped_column(ForeignKey("molecules.name"), primary_key=True)
    molecule : Mapped["Molecule"]= relationship(back_populates='reactions')
    reaction : Mapped["Reaction"]= relationship(back_populates = 'molecules')
    stoichiometry: Mapped[int]

class Molecule(Base):
    __tablename__ = "molecules"
    name: Mapped[str] = mapped_column(primary_key=True)
    elements: Mapped[List["AtomsPerMolecule"]] = relationship(back_populates="molecule")
    reactions: Mapped[List["Participant"]] = relationship(back_populates= "molecule")
    def add_atom(self, number, symbol):
        atom = element_factory(symbol)
        result = AtomsPerMolecule(number = number)
        result.element = atom
        self.elements.append(result)
        return result 

class Reaction(Base):
    __tablename__ = "reactions"
    id : Mapped[int]= mapped_column(primary_key=True)
    molecules : Mapped[List[Participant]] = relationship(back_populates = "reaction")
    def add_participant(self, stoichiometry, molecule):
        result = Participant(stoichiometry=stoichiometry)
        result.molecule=molecule
        self.molecules.append(result)
        return result
    
    def reactants(self):
        for participant in self.molecules:
            if participant.stoichiometry <0 :
                yield participant

    def products(self):
        for participant in self.molecules:
            if participant.stoichiometry >0 :
                yield participant
    


def create_tables(engine):
    Base.metadata.create_all(engine)

def drop_tables(engine):
    Base.metadata.drop_all(engine)

def session(engine):
    return sessionmaker(bind = engine)()

def add_items(items, session):
    count = len(items)
    for (n, item) in enumerate(items):
        logger.info(f"Saving reaction {n}/{count}")
        add_item(item, session)

def add_item(item, session):
    logger.debug(f"Saving reaction")
    session.add(item)
    session.flush()

from contextlib import contextmanager

@contextmanager
def sqlite():
    engine = create_engine('sqlite:///test.db')
    yield engine
    try:
        os.remove('test.db')
    except FileNotFoundError:
        pass # If we're using nested managers, this can happen.

@contextmanager
def sqlite_file():
    yield 'sqlite:///test.db'
    try:
        os.remove('test.db')
    except FileNotFoundError:
        pass # If we're using nested managers, this can happen.