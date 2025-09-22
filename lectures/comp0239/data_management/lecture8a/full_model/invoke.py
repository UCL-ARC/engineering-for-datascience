from argparse import ArgumentParser
from sqlalchemy import create_engine

from .transformer import files_to_model, ORD_to_SQLAlchemy, reaction_to_structure
from .model import add_items, session, create_tables

from rdkit import RDLogger

import logging


logger = logging.getLogger('ETL')
logger.setLevel(logging.INFO) # The default level for running tests etc

parser = ArgumentParser(description="Import the data from ORD")

parser.add_argument('--url', "-u", help="URL for remote connection")
parser.add_argument('--data', "-d", help="Path to a folder containing Protocol Buffer ORD messages")
parser.add_argument("--verbose", "-v", action='count', default = 0 )
parser.add_argument("--create", "-c", help="Create the database tables", action="store_true")
parser.add_argument("--no_upload", "-n", help="Parse the data, but don't attempt to send to the database", action="store_true")

def invoke_entry():
    invoke(parser.parse_args())
    
def invoke(arguments):

    ch = logging.StreamHandler()
    formatter = logging.Formatter("{asctime} {name} {levelname} : {message}",style="{")
    ch.setFormatter(formatter)
    logger.addHandler(ch)

    levels = [logging.ERROR, logging.WARNING, logging.INFO, logging.DEBUG]
    log_level = levels[min(arguments.verbose,3)]
    sql_log_level = levels[max(arguments.verbose - 2,0)]
    smiles_log_level = levels[max(arguments.verbose - 3,0)]
    logger.setLevel(log_level)
    
    logging.getLogger("sqlalchemy").setLevel(sql_log_level)
    logging.getLogger('pysmiles').setLevel(smiles_log_level)  

    RDLogger.DisableLog('rdApp.info')  

    if arguments.s3:
        logger.debug(f"Uploading ORD to s3 bucket {arguments.url} as JSON")


    if arguments.url:
        logger.debug(f"Databse URL {arguments.url}")
        connection = create_engine(arguments.url, logging_name = "ETL")
        logger.info("Connected to database")

    if arguments.create:
        create_tables(connection)

    if arguments.data:
        logger.info("Begin dataset transformation")
        if arguments.no_upload:
            s = False
        else:
            logger.info("... and upload.")
            s = session(connection)
        transform(arguments.data, s)
        logger.debug("Committing transaction.")
        s.commit()

    logger.info("Completed transformation")

def transform(path, database):

    model = files_to_model(path)
    data = ORD_to_SQLAlchemy(model, database)
    logger.info(f"Processed {len(data)} reactions.")
