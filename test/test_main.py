# Python
import os

# MySQL
import mysql.connector

# models
from models.seat_data import SeatData
from models.airplane_data import AirplaneData


def get_accounts(flight_id):
    db_host = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
    db_username = os.getenv("BSALE_AIRLINE_DB_USERNAME")
    db_password = os.getenv("BSALE_AIRLINE_DB_PASSWORD")
    cnx = mysql.connector.connect(
        host = db_host,
        user = db_username,
        password = db_password,
        database = "airline"
    )
    cursor = cnx.cursor()
    accounts_data_query: str = f'SELECT p.dni '\
                                f'FROM airline.boarding_pass AS bp '\
                                f'LEFT JOIN airline.passenger AS p '\
                                f'    ON bp.passenger_id = p.passenger_id '\
                                f'WHERE flight_id = {flight_id};'
    cursor.execute(accounts_data_query)
    accounts_data = cursor.fetchall()
    # accounts_data: list[AccountData] = [AccountData(**accounts_serializer(account)) for account in accounts_data]

    return accounts_data

def get_airplane_data(airplane_id):
    db_host = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
    db_username = os.getenv("BSALE_AIRLINE_DB_USERNAME")
    db_password = os.getenv("BSALE_AIRLINE_DB_PASSWORD")
    cnx = mysql.connector.connect(
        host = db_host,
        user = db_username,
        password = db_password,
        database = "airline"
    )
    cursor = cnx.cursor()
    airplane_data_query: str = f'SELECT s.seat_id, s.seat_column, s.seat_row, s.seat_type_id '\
                                    f'FROM airline.seat AS s '\
                                    f'WHERE s.airplane_id = {airplane_id}'
    cursor.execute(airplane_data_query)
    airplane_data = cursor.fetchall()
    airplane_data: AirplaneData = airplane_serializer(airplane_data)

    return airplane_data

def get_quantity_passengers_group_by_purchase_id(fligth_id):
    db_host = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
    db_username = os.getenv("BSALE_AIRLINE_DB_USERNAME")
    db_password = os.getenv("BSALE_AIRLINE_DB_PASSWORD")
    cnx = mysql.connector.connect(
        host = db_host,
        user = db_username,
        password = db_password,
        database = "airline"
    )
    cursor = cnx.cursor()
    query = f'select count(*) as quantity, bp.purchase_id '\
            f'from airline.boarding_pass as bp '\
            f'where bp.flight_id = {fligth_id} '\
            f'group by bp.purchase_id '\
            f'having quantity = 1 '\
            f'order by quantity desc;'
    cursor.execute(query)
    data = cursor.fetchall()
    list_to_return = []
    for d in data:
        list_to_return.append(d[1])
    return list_to_return

def get_around_seats(seat: SeatData, airplane: list[SeatData]):
    list_to_return = []
    right_seat = search_seat_by_col_and_row(
        chr(ord(seat.seatColumn) + 1),
        seat.seatRow,
        airplane
    )
    if right_seat:
        list_to_return.append(right_seat.seatId)
    left_seat = search_seat_by_col_and_row(
        chr(ord(seat.seatColumn) - 1),
        seat.seatRow,
        airplane
    )
    if left_seat:
        list_to_return.append(left_seat.seatId)
    next_seat = search_seat_by_col_and_row(
        seat.seatColumn,
        seat.seatRow - 1,
        airplane
    )
    if next_seat:
        list_to_return.append(next_seat.seatId)
    back_seat = search_seat_by_col_and_row(
        seat.seatColumn,
        seat.seatRow + 1,
        airplane
    )
    if back_seat:
        list_to_return.append(back_seat.seatId)
    return list_to_return
