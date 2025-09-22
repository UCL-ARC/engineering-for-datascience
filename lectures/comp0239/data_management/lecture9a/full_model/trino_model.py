from trino.dbapi import connect
import os
here = os.path.dirname(__file__)
model_path = os.path.join(here,"trino_model.sql")

import logging
logger = logging.getLogger('ETL')

def specify_external_table(cursor, uri):
     with open(model_path) as model:
          model_sql = model.read()
          model_sql_filled = model_sql.format(uri = uri)
          statements = model_sql_filled.split(';')
          for statement in statements:
            logger.debug(statement)
            print(statement)
            cursor.execute(statement)