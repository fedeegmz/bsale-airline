# SQLAlchemy
from sqlalchemy import MetaData, create_engine

# security
from security.config import settings


def conect_database():
    
    # load env
    db_host = settings.mysql_host
    db_port = settings.mysql_port
    db_username = settings.mysql_user
    db_password = settings.mysql_password
    print(f"Connect databse on '{db_host}:{db_port}'@'{db_username}'")

    engine = create_engine(
        f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/airline"
    )

    return engine.connect()


conn = conect_database()
meta = MetaData()

### Session ###
# from sqlalchemy.ext.declarative import declarative_base
# from sqlalchemy.orm import sessionmaker
# Base = declarative_base()
## Session into connect_database() ##
# Base.metadata.create_all(bind=engine)
# Session = sessionmaker(bind=engine)
# return Session()
