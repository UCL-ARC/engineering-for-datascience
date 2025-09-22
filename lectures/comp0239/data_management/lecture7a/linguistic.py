class Element:
    def __init__(self, symbol, number):
        self.symbol = symbol
        self.number = number
        
    def __str__(self):
        return str(self.symbol)
        
class Molecule:
    def __init__(self, mass):
        self.elements= {} # Map from element to number of that element in the molecule
        self.mass = mass
        
    def add_element(self, element, number):
        self.elements[element] = number
    
    @staticmethod
    def as_subscript(number):
        if number==1:
            return ""
        
        if number<10:
            return "_"+str(number)
        else:
            return "_{"+str(number)+"}"
    
    def __str__(self):
        return ''.join(
            [str(element)+Molecule.as_subscript(self.elements[element])
             for element in self.elements])
  
class Reaction:
    def __init__(self):
        self.reactants = { } # Map from reactants to stoichiometries
        self.products = { } # Map from products to stoichiometries
        
    def add_reactant(self, reactant, stoichiometry):
        self.reactants[reactant] = stoichiometry
        
    def add_product(self, product, stoichiometry):
        self.products[product] = stoichiometry
    
    @staticmethod
    def print_if_not_one(number):
        if number==1:
            return ''
        else: return str(number)
    
    @staticmethod
    def side_as_string(side):
        return " + ".join(
            [Reaction.print_if_not_one(side[molecule]) + str(molecule)
             for molecule in side])
        
    def __str__(self):
        return (Reaction.side_as_string(self.reactants)+
        " \\rightarrow "+Reaction.side_as_string(self.products))
    
class System:
    def __init__(self):
        self.reactions=[]
    def add_reaction(self, reaction):
        self.reactions.append(reaction)
        
    def __str__(self):
        return "\n".join(self.reactions)

c=Element("C", 12)
o=Element("O", 8)
h=Element("H", 1)

co2 = Molecule(44.01)
co2.add_element(c,1)
co2.add_element(o,2)

h2o = Molecule(18.01)
h2o.add_element(h,2)
h2o.add_element(o,1)

o2 = Molecule(32.00)
o2.add_element(o,2)

glucose = Molecule(180.16)
glucose.add_element(c,6)
glucose.add_element(h,12)
glucose.add_element(o,6)

combustion = Reaction()
combustion.add_reactant(glucose,  1)
combustion.add_reactant(o2, 6)
combustion.add_product(co2, 6)
combustion.add_product(h2o, 6)

print(combustion)