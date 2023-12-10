# SQLAlchemy
from sqlalchemy import Table, Column, Integer

# database
from database.mysql_client import meta


BoardingPassTable = Table(
    "boarding_pass", meta,
    Column("boarding_pass_id", Integer, primary_key=True),
    Column("purchase_id", Integer),
    Column("passenger_id", Integer),
    Column("seat_type_id", Integer),
    Column("seat_id", Integer),
    Column("flight_id", Integer)
)
