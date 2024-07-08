# SQLAlchemy
from sqlalchemy import (
    Table,
    Column,
    Integer,
    String
)

# database
from database.mysql_client import meta


FlightTable = Table(
    "flight",
    meta,
    Column(
        "flight_id",
        Integer,
        primary_key = True
    ),
    Column(
        "takeoff_date_time",
        Integer
    ),
    Column(
        "takeoff_airport",
        String(255)
    ),
    Column(
        "landing_date_time",
        Integer
    ),
    Column(
        "landing_airport",
        String(255)
    ),
    Column(
        "airplane_id",
        Integer
    )
)
