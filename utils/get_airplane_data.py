# SQLAlchemy
from sqlalchemy import select

# database
from database.mysql_client import conn

# schemas
from schemas.seat import SeatTable

# models
from models.seat_data import SeatData
from models.airplane_data import AirplaneData


def get_airplane_data(airplane_id: int) -> AirplaneData | None:
    airplane_result = conn.execute(
        select(
            SeatTable
        ).where(
            SeatTable.c.airplane_id == airplane_id
        ).order_by(
            SeatTable.c.seat_column,
            SeatTable.c.seat_row
        )
    ).all()
    if not airplane_result:
        return None

    return AirplaneData(
        seats = [SeatData(*item) for item in airplane_result]
    )
