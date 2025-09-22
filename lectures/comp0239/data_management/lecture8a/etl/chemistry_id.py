import numpy

class Element:
    def __init__(self, symbol, id):
        self.symbol = symbol
        self.id = id
        
class Molecule:
    def __init__(self, id):
        self.elements= {} # Map from element to number of that element in the molecule
        self.id=id
        
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
    
class System: # This will be our factory
    def __init__(self):
        self.reactions=[]
        self.elements=[]
        self.molecules=[]
        
    def add_element(self, symbol):
        new_element = Element(symbol, len(self.elements))
        self.elements.append(new_element)
        return new_element
    
    def add_molecule(self):
        new_molecule = Molecule(len(self.molecules))
        self.molecules.append(new_molecule)
        return new_molecule
    
    def add_reaction(self):
        new_reaction=Reaction()
        self.reactions.append(new_reaction)
        return new_reaction

    def save(self):
                    
        result = {
            'elements' : [element.symbol
                          for element in self.elements],
            'molecules' : {
                molecule.id:
                    {element.id: number
                          for element, number
                          in molecule.elements.items()}
                    for molecule in self.molecules},
            'reactions' : [{
                'reactants' : {
                        reactant.id : stoich
                        for reactant, stoich
                        in reaction.reactants.items()
                },
                'products' : {
                    product.id : stoich
                        for product, stoich
                        in reaction.products.items()
                    
                }}
                for reaction in self.reactions]
            }

        
        return result

    def __str__(self):
        return str(self.to_struct()).replace("'",'"')

class FakeSaveBinary: # Pretend binary-style writing to a list
    # to make it easier to read at first.    
    def save(self, system, buffer):
        buffer.append(len(system.elements))
        for element in system.elements:
            buffer.append(element.symbol)
        
        buffer.append(len(system.molecules))
        for molecule in system.molecules:
            buffer.append(len(molecule.elements))
            for element, number in molecule.elements.items():
                buffer.append(element.id)
                buffer.append(number)
        
        buffer.append(len(system.reactions))
        for reaction in system.reactions:
            buffer.append(len(reaction.reactants))
            for reactant, stoich in reaction.reactants.items():
                buffer.append(reactant.id)
                buffer.append(stoich)
            buffer.append(len(reaction.products))
            for product, stoich in reaction.products.items():
                buffer.append(product.id)
                buffer.append(stoich)

class XDRSavingSystem(System):
    
    def __init__(self, system):
        # Shallow Copy constructor
        self.elements = system.elements
        self.reactions = system.reactions
        self.molecules = system.molecules
        
    def save(self):
                 
        import xdrlib
        
        buffer = xdrlib.Packer()
        
        el_symbols = list(map(lambda x: x.symbol.encode('utf-8'), 
                                   self.elements))
        buffer.pack_array(el_symbols,
                          buffer.pack_string)
        #AUTOMATICALLY packs the length of the array first!

        def _pack_pair(item):
             buffer.pack_int(item[0].id)
             buffer.pack_int(item[1])
        
        def _pack_molecule(mol):
            buffer.pack_array(mol.elements.items(), 
                              _pack_pair)
        
        buffer.pack_array(self.molecules, _pack_molecule)
        
        def _pack_reaction(reaction):
            buffer.pack_array(reaction.reactants.items(),
                            _pack_pair)
            buffer.pack_array(reaction.products.items(),
                             _pack_pair)
        
        buffer.pack_array(self.reactions, _pack_reaction)
        return buffer

class HDF5SavingSystem(System):
    def __init__(self, system):
        # Shallow Copy constructor
        self.elements = system.elements
        self.reactions = system.reactions
        self.molecules = system.molecules
        
    def element_symbols(self):
        return list(map(lambda x: x.symbol.encode('ascii'), 
                                   self.elements))
    
    def molecule_matrix(self):
        molecule_matrix = numpy.zeros((len(self.elements), 
                                    len(self.molecules)),dtype=int)
        
        for molecule in self.molecules:
            for element, n in molecule.elements.items():
                molecule_matrix[element.id,
                            molecule.id]=n
            
        return molecule_matrix
    
    def reaction_matrix(self):
        reaction_matrix = numpy.zeros((len(self.molecules), 
                                    len(self.reactions)),dtype=int)
        
        for i, reaction in enumerate(self.reactions):
            for reactant,n in reaction.reactants.items():
                reaction_matrix[reactant.id,i]=-1*n
            
            for product, n in reaction.products.items():
                reaction_matrix[product.id,i]=n
    
        return reaction_matrix
    
    def write(self, filename):
        import h5py
        hdf = h5py.File(filename,'w')
        string_type = h5py.special_dtype(vlen=bytes)
        hdf.create_dataset('symbols', (len(self.elements),1),
                           string_type, self.element_symbols())
        hdf.create_dataset('molecules', data=self.molecule_matrix())
        hdf.create_dataset('reactions', data=self.reaction_matrix())
        hdf.close()