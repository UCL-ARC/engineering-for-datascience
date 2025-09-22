from lxml import etree
tree = etree.parse(open('system.xml'))
transform=etree.XSLT(etree.XML(open("xmltotex.xsl").read()))
print(str(transform(tree)))