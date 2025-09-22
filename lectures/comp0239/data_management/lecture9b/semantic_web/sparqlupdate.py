from jinja2 import Template
from full_model.test.fixtures.tiny_db import tiny_db
from rdflib import Graph

mytemplate = Template(open('system.ttl.j2').read())
with open('system.ttl','w') as ttlfile:
    ttlfile.write((mytemplate.render(reactions=tiny_db())))

graph = Graph()
graph.parse("system.ttl", format="ttl")

results=graph.update(
    """INSERT { ?elementa arcr:inMoleculeWith ?elementb }
       WHERE {
          ?molecule arcr:hasElementQuantity ?a .
          ?a arcr:countedElement ?elementa .
          ?elementa arcr:symbol ?asymbol .
          ?molecule arcr:hasElementQuantity ?b .
          ?b arcr:countedElement ?elementb .
          ?elementb arcr:symbol ?bsymbol
       }
       """)

q = """
SELECT DISTINCT ?asymbol ?bsymbol
WHERE {
        ?moleculea arcr:inMoleculeWith ?moleculeb .
        ?elementa arcr:symbol ?asymbol .
        ?elementb arcr:symbol ?bsymbol
    }
"""

results = graph.query(q)

for row in results:
    print("Elements %s and %s are found in the same molecule" % row)