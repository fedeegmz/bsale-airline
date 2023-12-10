# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String

# database
from database.mysql_client import meta


PassengerTable = Table(
    "passenger", meta,
    Column("passenger_id", Integer, primary_key=True),
    Column("dni", String(255)),
    Column("name", String(255)),
    Column("age", Integer),
    Column("country", String(255))
)
