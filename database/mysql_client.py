# SQLAlchemy
from sqlalchemy import MetaData, create_engine

# MySQL
# import mysql.connector

# security
from security.config import settings


def conect_database():
    
    # load env
    db_host = settings.mysql_host
    db_port = settings.mysql_port
    db_username = settings.mysql_user
    db_password = settings.mysql_password
    print(db_host, db_username, db_password)

    engine = create_engine(
        f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/airline"
    )

    return engine.connect()


conn = conect_database()
meta = MetaData()
