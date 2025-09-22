from full_model.test.fixtures.tiny_db import tiny_db
from jinja2 import Template

mytemplate = Template(open('chemistry_template.j2').read())
with open('system.xml','w') as xmlfile:
    xmlfile.write((mytemplate.render( reactions = tiny_db())))