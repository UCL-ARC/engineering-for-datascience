from lxml import etree
tree = etree.parse(open('system.xml'))
print(tree.xpath('//molecule/element[@number="1"]/@symbol'))