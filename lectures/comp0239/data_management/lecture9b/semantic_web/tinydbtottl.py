from jinja2 import Template
from full_model.test.fixtures.tiny_db import tiny_db

mytemplate = Template(open('system.ttl.j2').read())
with open('system.ttl','w') as ttlfile:
    ttlfile.write((mytemplate.render(reactions=tiny_db())))