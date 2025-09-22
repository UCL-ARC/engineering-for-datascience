from .fixtures.trino import remote_trino
from ..helpers import json_to_s3

def test_remote_trino_write_s3():

    with remote_trino("development") as cursor:
        cursor.execute("""
                        CREATE SCHEMA hive.s3 WITH (
                        location='s3a://reactions239-development/test')
                        """)
        cursor.execute("""
                       CREATE TABLE hive.s3.numbers (
                        number INTEGER
                       ) WITH (
                        format='JSON'
                       )
                       """)
        cursor.execute("INSERT INTO hive.s3.numbers VALUES (1)")
        cursor.execute("SELECT * FROM hive.s3.numbers")
        assert(cursor.fetchone() == [1])
        cursor.execute("DROP TABLE hive.s3.numbers")
        cursor.execute("DROP SCHEMA hive.s3")

def test_remote_trino_write_s3_nested():
    # Creates this JSON in s3:
    # "age":47,"name":{"given":"James","family":"Hetherington"}}


    with remote_trino("development") as cursor:
        cursor.execute("""
                        CREATE SCHEMA hive.s3 WITH (
                        location='s3a://reactions239-development/test')
                        """)
        cursor.execute("""
                       CREATE TABLE hive.s3.people (
                        age INTEGER,
                        name ROW (
                            given varchar,
                            family varchar )
                       ) WITH (
                        format='JSON'
                       )
                       """)
        cursor.execute("INSERT INTO hive.s3.people VALUES (47, ('James', 'Hetherington'))")
        cursor.execute("SELECT * FROM hive.s3.people")
        assert(cursor.fetchone() == [47,("James","Hetherington")])
        cursor.execute("DROP TABLE hive.s3.people")
        cursor.execute("DROP SCHEMA hive.s3")

def test_remote_insert_json_to_s3_trino_read():

    data = {"age":47,"name":{"given":"James","family":"Hetherington"}}
    json_to_s3("reactions239-development", "test/external_people/example.json", data)
    with remote_trino("development") as cursor:
        cursor.execute("""
                CREATE SCHEMA hive.s3 WITH (
                location='s3a://reactions239-development/test')
                """)
        cursor.execute("""
                       CREATE TABLE hive.s3.people (
                        age INTEGER,
                        name ROW (
                            given varchar,
                            family varchar )
                       ) WITH (
                        format='JSON',
                        external_location = 's3a://reactions239-development/test/external_people'
                       )
                       """)
        # NOTE THERE IS NO INSERT STATEMENT
        cursor.execute("SELECT * FROM hive.s3.people")
        assert(cursor.fetchone() == [47,("James","Hetherington")])
        cursor.execute("DROP TABLE hive.s3.people")
        cursor.execute("DROP SCHEMA hive.s3")
