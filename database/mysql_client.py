# FastAPI
from fastapi import HTTPException, status

# MySQL
import mysql.connector

# security
from security.config import settings


class MySQLClient():

    def __init__(self) -> None:
        
        # load env
        db_host = settings.mysql_host
        db_username = settings.mysql_user
        db_password = settings.mysql_password

        try:
            cnx = mysql.connector.connect(
                host = db_host,
                user = db_username,
                password = db_password,
                database = "airline"
            )
            self.cursor = cnx.cursor()
        except:
            raise HTTPException(
                status_code = status.HTTP_400_BAD_REQUEST,
                detail = {
                    "code": 400,
                    "errors": "could not connect to db"
                }
            )

cursor = MySQLClient().cursor
