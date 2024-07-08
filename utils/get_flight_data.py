# SQLAlchemy
from sqlalchemy import select

# database
from database.mysql_client import conn

# schemas
from schemas.flight import FlightTable

# models
from models.flight_data import FlightData


def get_flight_data(flight_id: int) -> FlightData | None:
    flight_result = conn.execute(
        select(
            FlightTable
        ).where(
            FlightTable.c.flight_id == flight_id
        )
    ).first()
    if not flight_result:
        return None

    return FlightData(*flight_result)
