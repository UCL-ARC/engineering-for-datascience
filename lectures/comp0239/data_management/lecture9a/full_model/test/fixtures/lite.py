
import sqlalchemy, os
from contextlib import contextmanager

@contextmanager
def sqlite():
    engine = sqlalchemy.create_engine('sqlite:///test.db')
    yield engine
    try:
        os.remove('test.db')
    except FileNotFoundError:
        pass # If we're using nested managers, this can happen.

@contextmanager
def sqlite_file():
    yield 'sqlite:///test.db'
    try:
        os.remove('test.db')
    except FileNotFoundError:
        pass # If we're using nested managers, this can happen.