from chemistry_id import System
import yaml

if __name__ == '__main__':

    system = System()

    c = system.add_element('C')
    o = system.add_element('O')
    h = system.add_element('H')

    carbon_dioxide = system.add_molecule()
    carbon_dioxide.add_element(c,1)
    carbon_dioxide.add_element(o,2)

    water = system.add_molecule()
    water.add_element(h,2)
    water.add_element(o,1)

    oxygen = system.add_molecule()
    oxygen.add_element(o,2)

    hydrogen = system.add_molecule()
    hydrogen.add_element(h,2)

    glucose = system.add_molecule()
    glucose.add_element(c,6)
    glucose.add_element(h,12)
    glucose.add_element(o,6)

    methane = system.add_molecule()
    methane.add_element(c,1)
    methane.add_element(h,4)

    burning_glucose = system.add_reaction()
    burning_glucose.add_reactant(glucose,1)
    burning_glucose.add_reactant(oxygen,6)
    burning_glucose.add_product(carbon_dioxide, 6)
    burning_glucose.add_product(water, 6)

    burning_hydrogen = system.add_reaction()
    burning_hydrogen.add_reactant(hydrogen,2)
    burning_hydrogen.add_reactant(oxygen,1)    
    burning_hydrogen.add_product(water, 2)

    burning_methane = system.add_reaction()
    burning_methane.add_reactant(methane,1)
    burning_methane.add_reactant(oxygen, 2)
    burning_methane.add_product(carbon_dioxide,1)
    burning_methane.add_product(water,2)

    print(yaml.dump(system.save()))