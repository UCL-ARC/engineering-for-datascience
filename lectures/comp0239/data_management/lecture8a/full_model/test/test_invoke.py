from ..invoke import parser, invoke
from .fixtures.lite import sqlite, sqlite_file
from .fixtures.ord import small, folder
from ..model import session, Molecule

def test_create():
    args = parser.parse_args("--create --url sqlite:///test.db -vvv".split())
    assert args.url == "sqlite:///test.db"
    assert args.create
    with sqlite_file(): #Ensure the file is deleted after the test
        invoke(args)

        with sqlite() as db:
            pass # Should write a test to check the table is present

def test_upload():
    args = parser.parse_args(f"--create --url sqlite:///test.db -vvv --data {small}".split())
    assert args.url == "sqlite:///test.db"
    assert args.create
    with sqlite_file():
        invoke(args)

        with sqlite() as db:
            s= session(db)
            mol = s.get(Molecule,'H32C27O3N4F2')
            assert mol
    
def test_upload_folder():
    args = parser.parse_args(f"--create --url sqlite:///test.db -vvv --data {folder}/**/*".split())
    assert args.url == "sqlite:///test.db"
    assert args.create
    with sqlite_file():
        invoke(args)

        with sqlite() as db:
            s= session(db)
            mol = s.get(Molecule,'H32C27O3N4F2')
            assert mol
