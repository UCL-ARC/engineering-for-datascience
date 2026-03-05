from trino.dbapi import connect
import contextlib
from trino.auth import BasicAuthentication

@contextlib.contextmanager
def remote_trino(stage):
    conn = connect(
        host="ucgajhe-trino.comp0235.condenser.arc.ucl.ac.uk",
        #host="localhost",
        port=443, #80, or 80 for local
        user="user",
        catalog="hive",
        auth = BasicAuthentication("user", "*****"),
    )
    cur = conn.cursor()
    yield cur