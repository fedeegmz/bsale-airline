# models
from models.seat_data import SeatData
from models.airplane_data import AirplaneData


def get_around_seats(
    seat_id: int,
    airplane: AirplaneData
) -> list[SeatData | None]:
    seat = airplane.search_seat_by_id(seat_id)

    list_to_return = []
    right_seat = airplane.search_seat_by_col_and_row(
        chr(ord(seat.seat_column) + 1),
        seat.seat_row
    )
    if right_seat:
        list_to_return.append(right_seat.seat_id)
    left_seat = airplane.search_seat_by_col_and_row(
        chr(ord(seat.seat_column) - 1),
        seat.seat_row
    )
    if left_seat:
        list_to_return.append(left_seat.seat_id)
    next_seat = airplane.search_seat_by_col_and_row(
        seat.seat_column,
        seat.seat_row - 1
    )
    if next_seat:
        list_to_return.append(next_seat.seat_id)
    back_seat = airplane.search_seat_by_col_and_row(
        seat.seat_column,
        seat.seat_row + 1
    )
    if back_seat:
        list_to_return.append(back_seat.seat_id)
    return list_to_return
