# models
from models.seat_data import SeatData
from models.airplane_data import AirplaneData


def airplane_serializer(data: list):
    list_to_return = []
    for seat in data:
        list_to_return.append(
            SeatData(
                **{
                    "seatId": int(seat[0]),
                    "seatColumn": seat[1],
                    "seatRow": int(seat[2]),
                    "seatTypeId": int(seat[3])
                }
            )
        )
    return AirplaneData(seats=list_to_return)