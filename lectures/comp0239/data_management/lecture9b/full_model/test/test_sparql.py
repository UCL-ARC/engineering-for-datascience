from .fixtures.sparql import remote_sparql, remote_sparql_update

def test_remote_sparql_exists():
    with remote_sparql_update("development") as writer:
        insert = """
            INSERT DATA {
                <http://exampleSub> <http://examplePred> <http://exampleObj> .
            }
        """
        writer.setQuery(insert)
        result = writer.query()

    with remote_sparql("development") as sparql:
        sparql.setQuery("SELECT ?subject WHERE {?subject ?p ?o}")
        result = sparql.queryAndConvert()['results']['bindings'][0]
        print(result)
        assert result["subject"]['value'] == "http://exampleSub" 