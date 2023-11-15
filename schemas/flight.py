# SQLAlchemy
from sqlalchemy import Table, Column, Integer, String
# from sqlalchemy.orm import declarative_base

# database
from database.mysql_client import meta


# Base = declarative_base()

flight = Table(
    "flight", meta,
    Column("flight_id", Integer, primary_key=True),
    Column("takeoff_date_time", Integer),
    Column("takeoff_airport", String(255)),
    Column("landing_date_time", Integer),
    Column("landing_airport", String(255)),
    Column("airplane_id", Integer)
)
# class FlightORM(Base):
#     __tablename__ = "flight"

#     flight_id = Column(Integer, primary_key=True)
#     takeoff_date_time = Column(Integer)
#     takeoff_airport = Column(String(255))
#     landing_date_time = Column(Integer)
#     landing_airport = Column(String(255))
#     airplane_id = Column(Integer)
