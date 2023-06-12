import os
import mysql.connector

# MySQL -> airline
db_host = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
db_username = os.getenv("BSALE_AIRLINE_DB_USERNAME")
db_password = os.getenv("BSALE_AIRLINE_DB_PASSWORD")

cnx = mysql.connector.connect(
    host = db_host,
    user = db_username,
    passwor = db_password,
    database = "airline"
)
cursor = cnx.cursor()