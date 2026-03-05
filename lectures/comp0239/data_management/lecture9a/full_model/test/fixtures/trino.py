from trino.dbapi import connect
import contextlib

@contextlib.contextmanager
def remote_trino(stage):
    conn = connect(
        #E.g. host="ucgajhe-trino.comp0235.condenser.arc.ucl.ac.uk",
        host="localhost",
        port=80, #or 443 for over condenser ingress
        user="almalinux",
        catalog="hive"
    )
    cur = conn.cursor()
    yield cur