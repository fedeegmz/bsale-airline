# SQLAlchemy
from sqlalchemy import Table, Column, Integer

# database
from database.mysql_client import meta


purchase = Table(
    "purchase", meta,
    Column("purchase_id", Integer, primary_key=True),
    Column("purchase_date", Integer)
)
