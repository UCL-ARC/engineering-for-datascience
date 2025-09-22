from lxml import etree
schema = etree.XMLSchema(etree.XML(open("reactions.xsd").read()))
parser = etree.XMLParser(schema = schema)
tree = etree.parse(open('system.xml'),parser)
print(tree)