import yaml
import json
import os
import contextlib
import subprocess
from sqlalchemy import create_engine
import psycopg2

def user_and_password():
    ansible = os.path.join(os.path.dirname(
      os.path.dirname(os.path.dirname(__file__))),'..')
    print(ansible)
    password = ""
    with open(os.path.join(ansible,'.postgrespass'), 'r') as passfile:
        password = passfile.read().rstrip()
    user = "almalinux"

    return (user, password)

def remote_host(stage):
    ansible = os.path.join(os.path.dirname(
      os.path.dirname(os.path.dirname(__file__))),'..')
    print(ansible)
    ip_data = json.loads(subprocess.run("terraform output --json primary_ips".split(), cwd=ansible, capture_output=True, encoding='UTF-8').stdout)
    ip_addr = ip_data.pop()
    return ip_addr

@contextlib.contextmanager
def remote_cursor(stage):
    (user, password) = user_and_password()
    host = remote_host(stage)

    with psycopg2.connect(database='molecules',user=user,password=password,
                            host = host, port=5432) as connection:
        with connection.cursor() as cursor:
            yield cursor

@contextlib.contextmanager
def remote(stage):
    (user, password) = user_and_password()
    host = remote_host(stage)
    yield create_engine(f"postgresql+psycopg2://{user}:{password}@{host}/molecules?sslmode=require")