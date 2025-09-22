with open('/home/almalinux/.postgrespass', 'r') as passwordfile:
    password = passwordfile.read().rstrip()
server = ""
username = "almalinux"
database = "molecules_sqla"
engine = sqlalchemy.create_engine(f'postgresql+psycopg2://{username}:{password}@{server}/{database}?sslmode=verify-full')
