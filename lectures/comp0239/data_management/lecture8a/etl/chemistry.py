class Element:
    def __init__(self, symbol):
        self.symbol = symbol
   
class Molecule:
    def __init__(self):
        self.elements= {} # Map from element to number of that element in the molecule
        
    def add_element(self, element, number):
        self.elements[element] = number
    
    def to_struct(self):
        return {x.symbol: self.elements[x] for x in self.elements}
 
    def __str__(self):
        return str(self.to_struct()).replace("'",'"')

class Reaction:
    def __init__(self):
        self.reactants = { } # Map from reactants to stoichiometries
        self.products = { } # Map from products to stoichiometries
        
    def add_reactant(self, reactant, stoichiometry):
        self.reactants[reactant] = stoichiometry
        
    def add_product(self, product, stoichiometry):
        self.products[product] = stoichiometry
        
    def to_struct(self):
        return {
            'reactants' : [x.to_struct() for x in self.reactants],
            'products' : [x.to_struct() for x in self.products],
            'stoichiometries' : list(self.reactants.values())+
                                list(self.products.values())
        }

    def __str__(self):
        return str(self.to_struct()).replace("'",'"')

class System:
    def __init__(self):
        self.reactions=[]
    def add_reaction(self, reaction):
        self.reactions.append(reaction)
        
    def to_struct(self):
        return [x.to_struct() for x in self.reactions]

    def __str__(self):
        return str(self.to_struct()).replace("'",'"')

class DeSerialiseStructure:
    def __init__(self):
        self.elements = {}
        self.molecules = {}
        
    def add_element(self, candidate):
        if candidate not in self.elements:
            self.elements[candidate]=Element(candidate)
        return self.elements[candidate]
    
    def add_molecule(self, candidate):
        if tuple(candidate.items()) not in self.molecules:
            m = Molecule()
            for symbol, number in candidate.items():
                m.add_element(self.add_element(symbol), number)
            self.molecules[tuple(candidate.items())]=m
        return self.molecules[tuple(candidate.items())]
    
    def parse_system(self, json_struct):
        s = System()
        for reaction in json_struct:
            r = Reaction()
            stoichiometries = reaction['stoichiometries']
            for molecule in reaction['reactants']:
                r.add_reactant(self.add_molecule(molecule),
                               stoichiometries.pop(0))
            for molecule in reaction['products']:
                r.add_product(self.add_molecule(molecule),
                               stoichiometries.pop(0))
            s.add_reaction(r)
        return s

class SaveSystem:
    def __init__(self):
        self.elements = set()
        self.molecules = set()
        
    def element_key(self, element):
        
        return element.symbol
    
    def molecule_key(self, molecule):
        key=''
        for element, number in molecule.elements.items():
            key+=element.symbol
            key+=str(number)
        return key
    
    def save(self, system):
        for reaction in system.reactions:
            for molecule in reaction.reactants:
                self.molecules.add(molecule)
                for element in molecule.elements:
                    self.elements.add(element)
            for molecule in reaction.products:
                self.molecules.add(molecule)
                for element in molecule.elements:
                    self.elements.add(element)
                    
        result = {
            'elements' : [self.element_key(element)
                          for element in self.elements],
            'molecules' : {
                self.molecule_key(molecule):
                    {self.element_key(element): number
                          for element, number
                          in molecule.elements.items()}
                    for molecule in self.molecules},
            'reactions' : [{
                'reactants' : {
                    self.molecule_key(reactant) : stoich
                        for reactant, stoich
                        in reaction.reactants.items()
                },
                'products' : {
                    self.molecule_key(product) : stoich
                        for product, stoich
                        in reaction.products.items()
                    
                }}
                for reaction in system.reactions]
            }
        return result

class SaveSystemI:
    def __init__(self):
        self.elements = {}
        self.molecules = {}
        
    def add_element(self, element):
        if element not in self.elements:
            self.elements[element]=len(self.elements)
        return self.elements[element]
        
    def add_molecule(self, molecule):
        if molecule not in self.molecules:
            self.molecules[molecule]=len(self.molecules)
        return self.molecules[molecule]
        
    def element_key(self, element):
        return self.elements[element]
    
    def molecule_key(self, molecule):
        return self.molecules[molecule]
    
    def save(self, system):
        for reaction in system.reactions:
            for molecule in reaction.reactants:
                self.add_molecule(molecule)
                for element in molecule.elements:
                    self.add_element(element)
            for molecule in reaction.products:
                self.add_molecule(molecule)
                for element in molecule.elements:
                    self.add_element(element)
                    
        result = {
            'elements' : [element.symbol
                          for element in self.elements],
            'molecules' : {
                self.molecule_key(molecule):
                    {self.element_key(element): number
                          for element, number
                          in molecule.elements.items()}
                    for molecule in self.molecules},
            'reactions' : [{
                'reactants' : {
                    self.molecule_key(reactant) : stoich
                        for reactant, stoich
                        in reaction.reactants.items()
                },
                'products' : {
                    self.molecule_key(product) : stoich
                        for product, stoich
                        in reaction.products.items()
                    
                }}
                for reaction in system.reactions]
            }
        return result