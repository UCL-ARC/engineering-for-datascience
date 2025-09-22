from .fixtures.trino import remote_trino
from .fixtures.ord import small
from ..transformer import file_to_model, reaction_to_structure
from ..helpers import json_to_s3
from ..trino_model import specify_external_table

def test_remote_trino_model():
    small_model = file_to_model(small)
    first = small_model[0]
    structure = reaction_to_structure(first)
    json_to_s3("reactions239-development", "test/reactions/reactions/first.json", structure)

    with remote_trino("development") as cursor:
        specify_external_table(cursor, "s3a://reactions239-development/test")
        cursor.execute("SELECT * FROM hive.reactions.reactions")
        result = cursor.fetchone()
        assert result[1][-1][1] == 32 
        cursor.execute("DROP TABLE hive.reactions.reactions")
        cursor.execute("DROP SCHEMA hive.reactions")