from rdflib import Graph

graph = Graph()
graph.parse("reaction.ttl", format="ttl")

print(len(graph)) # prints 1

for statement in graph:
    print(statement)

print(graph.serialize(format='xml'))