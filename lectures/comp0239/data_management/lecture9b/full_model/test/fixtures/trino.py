from trino.dbapi import connect
import contextlib

@contextlib.contextmanager
def remote_trino(stage):
    conn = connect(
        host="localhost",
        port=80,
        user="almalinux",
        catalog="hive"
    )
    cur = conn.cursor()
    yield cur