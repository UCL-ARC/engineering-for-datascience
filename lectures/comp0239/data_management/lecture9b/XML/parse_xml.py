from lxml import etree
tree = etree.parse(open('system.xml'))
print(tree.getroot()[0][0][1].attrib['stoichiometry'])