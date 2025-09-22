from chemistry import Element, Molecule, Reaction

def tiny_db():
    water = Molecule(name='water')
    oxygen_m = Molecule(name='oxygen')
    hydrogen_m = Molecule(name='hydrogen')

    water.add_atom(1, 'O')
    water.add_atom(2, 'H')
    oxygen_m.add_atom(2, 'O')
    hydrogen_m.add_atom(2, 'H')
    
    water_formation = Reaction()
    water_formation.add_participant(-2, hydrogen_m)
    water_formation.add_participant(-1, oxygen_m)
    water_formation.add_participant(2, water)

    water_breakup = Reaction()
    water_breakup.add_participant(2, hydrogen_m)
    water_breakup.add_participant(1, oxygen_m)
    water_breakup.add_participant(-2, water)
   
    return [water_formation, water_breakup]

if __name__ == "__main__":
    print(tiny_db())