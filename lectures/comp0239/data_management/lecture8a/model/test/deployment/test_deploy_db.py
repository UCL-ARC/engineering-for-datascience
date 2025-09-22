from ..fixtures.remote_db import remote_cursor

def test_deploy_remote_development_present():
    verify_remote_db_server_present('dev')

def test_deploy_remote_testing_present():
    verify_remote_db_server_present('test')

def verify_remote_db_server_present(stage):
    # Assert that we have created a Postgres server, and that we can connect to it
    with remote_cursor(stage) as cursor:
        cursor.execute("CREATE TABLE numbers (number INTEGER)")
        cursor.execute("INSERT INTO numbers VALUES (1)")
        cursor.execute("SELECT * FROM numbers")
        assert(cursor.fetchone() == (1,))
        cursor.execute("DROP TABLE numbers")