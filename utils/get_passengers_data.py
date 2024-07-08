# SQLAlchemy
from sqlalchemy import select

# database
from database.mysql_client import conn

# schemas
from schemas.passenger import PassengerTable
from schemas.boarding_pass import BoardingPassTable

# models
from models.seat_data import SeatData
from models.passenger_data import PassengerData


def get_passengers_data(
    flight_id: int
) -> list[PassengerData] | None:
    passengers_result = conn.execute(
        select(PassengerTable, BoardingPassTable).join(
            BoardingPassTable,
            PassengerTable.c.passenger_id == BoardingPassTable.c.passenger_id
        ).where(
            BoardingPassTable.c.flight_id == flight_id
        ).order_by(
            BoardingPassTable.c.purchase_id,
            BoardingPassTable.c.seat_type_id,
            BoardingPassTable.c.seat_id.desc(), # DESC
            PassengerTable.c.age
        )
    ).all()
    if not passengers_result:
        return None

    return [
        PassengerData(*passenger) 
        for passenger in passengers_result
    ]
