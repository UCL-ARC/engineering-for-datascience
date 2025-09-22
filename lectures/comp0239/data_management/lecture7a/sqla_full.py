import sqlalchemy
from sqlalchemy import text

import os
try:
    os.remove('molecules.db')
    print("Remove database to teach again from scratch")
except FileNotFoundError:
    print("No DB since this notebook was last run")

engine = sqlalchemy.create_engine('sqlite:///molecules.db', echo=True)
    
from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey
metadata = MetaData()
molecules = Table('molecules', metadata,
                  Column('name', String, primary_key=True),
                  Column('mass', Float))

atoms = Table('atoms', metadata,
      Column('symbol', String, primary_key=True),
      Column('number', Integer)
             )

atoms_in_molecules = Table('atoms_molecules', metadata,
       Column('atom', None, ForeignKey('atoms.symbol')),
       Column('molecule', None, ForeignKey('molecules.name')),
       Column('number', Integer)
)

metadata.create_all(engine)

conn = engine.connect()

conn.execute(molecules.insert().values(name='water', mass='18.01'))
conn.execute(molecules.insert().values(name='oxygen', mass='16.00'))
conn.execute(atoms.insert().values(symbol='O', number=8))
conn.execute(atoms.insert().values(symbol='H', number=1))
conn.execute(atoms_in_molecules.insert().values(molecule='water',atom='O',number=1))
conn.execute(atoms_in_molecules.insert().values(molecule='oxygen',atom='O',number=2))
conn.execute(atoms_in_molecules.insert().values(molecule='water',atom='H', number=1))