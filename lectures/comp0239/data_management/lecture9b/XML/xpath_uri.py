from lxml import etree
tree = etree.parse(open('uriexample.xml'))
print("Without namespace: ")
print(tree.xpath('//molecule/element[@number="1"]/@symbol'))
print("With namepace: ")
namespaces={'r': 'http://arc.ucl.ac.uk/schema/reaction/'}
print(tree.xpath('//r:molecule/r:element[@number="1"]/@symbol', namespaces = namespaces))