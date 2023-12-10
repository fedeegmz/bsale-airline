# SQLAlchemy
from sqlalchemy import select

# database
from database.mysql_client import conn

# schemas
from schemas.flight import FlightTable


def get_flights_id_in_db() -> tuple:
    result = conn.execute(
        select(FlightTable.c.flight_id)
    )
    
    return tuple([item[0] for item in result])
