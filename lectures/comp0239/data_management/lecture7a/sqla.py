from sqlalchemy import Table, Column, Integer, Float, String, MetaData, ForeignKey, create_engine

engine = create_engine("sqlite:///:memory:", echo=True)
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