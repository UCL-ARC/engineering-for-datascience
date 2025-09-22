from chemistry import Molecule, Element, Reaction, System, SaveSystem
import yaml

if __name__ == '__main__':
    h = Element('H')
    c = Element('C')
    o = Element('O')

    carbon_dioxide = Molecule()
    carbon_dioxide.add_element(c,1)
    carbon_dioxide.add_element(o,2)

    oxygen = Molecule()
    oxygen.add_element(o,2)

    hydrogen = Molecule()
    hydrogen.add_element(h,2)

    water = Molecule()
    water.add_element(h,2)
    water.add_element(o,1)

    glucose = Molecule()
    glucose.add_element(c,6)
    glucose.add_element(h,12)
    glucose.add_element(o,6)

    methane = Molecule()
    methane.add_element(c,1)
    methane.add_element(h,4)

    burning_glucose = Reaction()
    burning_glucose.add_reactant(glucose,1)
    burning_glucose.add_reactant(oxygen,6)
    burning_glucose.add_product(carbon_dioxide, 6)
    burning_glucose.add_product(water, 6)

    burning_hydrogen = Reaction()
    burning_glucose.add_reactant(hydrogen,2)
    burning_glucose.add_reactant(oxygen,1)    
    burning_glucose.add_product(water, 2)

    burning_methane = Reaction()
    burning_methane.add_reactant(methane,1)
    burning_methane.add_reactant(oxygen, 2)
    burning_methane.add_product(carbon_dioxide,1)
    burning_methane.add_product(water,2)

    reactions = System()
    reactions.add_reaction(burning_glucose)
    reactions.add_reaction(burning_hydrogen)
    reactions.add_reaction(burning_methane)

    saver = SaveSystem()
    print(yaml.dump(saver.save(reactions)))