# FastAPI
from fastapi import (
    HTTPException,
    status
)

# SQLAlchemy
from sqlalchemy import (
    MetaData,
    create_engine
)

# security
from security.config import settings


def conect_database():
    
    # load env
    db_host = settings.mysql_host
    db_port = settings.mysql_port
    db_username = settings.mysql_user
    db_password = settings.mysql_password
    print(f"Connect databse on '{db_host}:{db_port}'@'{db_username}'")

    try:
        engine = create_engine(
            f"mysql+pymysql://{db_username}:{db_password}@{db_host}:{db_port}/airline"
        )
    except:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "code": 400,
                "errors": "could not connect to db"
            }
        )

    return engine.connect()


conn = conect_database()
meta = MetaData()
