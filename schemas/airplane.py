# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String

# database
from database.mysql_client import meta


AirplaneTable = Table(
    "airplane", meta,
    Column("airplane_id", Integer, primary_key=True),
    Column("name", String(255))
)
