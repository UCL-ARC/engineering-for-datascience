from SPARQLWrapper import SPARQLWrapper, JSON, POST

import contextlib

@contextlib.contextmanager
def remote_sparql(stage):
    server = "127.0.0.1"
    sparql = SPARQLWrapper(f"http://{server}:8080/rdf4j-server/repositories/reactions")
    sparql.setReturnFormat(JSON)
    yield sparql

@contextlib.contextmanager
def remote_sparql_update(stage):
    server = "127.0.0.1"
    sparql = SPARQLWrapper(f"http://{server}:8080/rdf4j-server/repositories/reactions/statements")
    sparql.setReturnFormat(JSON)
    sparql.setMethod(POST)
    yield sparql