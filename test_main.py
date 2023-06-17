import os
from fastapi.testclient import TestClient
import mysql.connector

from main import app
from models import AccountData, AirplaneData, SeatData
from serializers import accounts_serializer, airplane_serializer
from util import search_seat_by_id, search_seat_by_col_and_row

client = TestClient(app)

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
    accounts_data_query: str = f'SELECT p.dni'\
                                f'FROM airline.boarding_pass AS bp '\
                                f'LEFT JOIN airline.passenger AS p '\
                                f'    ON bp.passenger_id = p.passenger_id '\
                                f'WHERE flight_id = {flight_id}; '
    cursor.execute(accounts_data_query)
    accounts_data = cursor.fetchall()
    accounts_data: list[AccountData] = [AccountData(**accounts_serializer(account)) for account in accounts_data]

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

def get_around_seats(seat: SeatData, airplane):
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
        str(int(seat.seatRow) - 1),
        airplane
    )
    if next_seat:
        list_to_return.append(next_seat.seatId)
    back_seat = search_seat_by_col_and_row(
        seat.seatColumn,
        str(int(seat.seatRow) + 1),
        airplane
    )
    if back_seat:
        list_to_return.append(back_seat.seatId)
    return list_to_return

### flightData ###

def test_flight_data_for_flight_id_0():
    response = client.get("/flights/0/passengers")
    assert response.json() == {
        "detail": {
            "code": 404,
            "data": {}
        }
    }

def test_flight_data_for_flight_id_1():
    response = client.get("/flights/1/passengers")
    data = response.json().get("data")

    assert data.get("flightId") == 1
    assert data["takeoffDateTime"] == 1688207580
    assert data["takeoffAirport"] == "Aeropuerto Internacional Arturo Merino Benitez, Chile"
    assert data["landingDateTime"] == 1688221980
    assert data["landingAirport"] == "Aeropuerto Internacional Jorge Cháve, Perú"
    assert data["airplaneId"] == 1

def test_flight_data_for_flight_id_2():
    response = client.get("/flights/2/passengers")
    data = response.json().get("data")

    assert data.get("flightId") == 2
    assert data.get("takeoffDateTime") == 1688491980
    assert data.get("takeoffAirport") == "Aeropuerto Internacional Jorge Cháve, Perú"
    assert data.get("landingDateTime") == 1688495580
    assert data.get("landingAirport") == "Aeropuerto Francisco Carlé, Perú"
    assert data.get("airplaneId") == 2

def test_flight_data_for_flight_id_3():
    response = client.get("/flights/3/passengers")
    data = response.json().get("data")

    assert data.get("flightId") == 3
    assert data.get("takeoffDateTime") == 1688766182
    assert data.get("takeoffAirport") == "Aeropuerto El Tepual, Chile"
    assert data.get("landingDateTime") == 1688772962
    assert data.get("landingAirport") == "Aeropuerto Internacional Arturo Merino Benitez, Chile"
    assert data.get("airplaneId") == 2

def test_flight_data_for_flight_id_4():
    response = client.get("/flights/4/passengers")
    data = response.json().get("data")

    assert data.get("flightId") == 4
    assert data.get("takeoffDateTime") == 1689786902
    assert data.get("takeoffAirport") == "Aeropuerto Internacional Arturo Merino Benitez, Chile"
    assert data.get("landingDateTime") == 1689819302
    assert data.get("landingAirport") == "Aeropuerto Internacional de la Ciudad de México, México"
    assert data.get("airplaneId") == 1

def test_flight_data_for_flight_id_5():
    response = client.get("/flights/5/passengers")
    assert response.json() == {
        "detail": {
            "code": 404,
            "data": {}
        }
    }

### length of passengers ###

def test_length_passengers_for_flight_id_1():
    response = client.get("/flights/1/passengers")
    data = response.json().get("data")
    accounts = get_accounts(1)

    assert len(accounts) == len(data.get("passengers"))

def test_length_passengers_for_flight_id_2():
    response = client.get("/flights/2/passengers")
    data = response.json().get("data")
    accounts = get_accounts(2)

    assert len(accounts) == len(data.get("passengers"))

def test_length_passengers_for_flight_id_3():
    response = client.get("/flights/3/passengers")
    data = response.json().get("data")
    accounts = get_accounts(3)

    assert len(accounts) == len(data.get("passengers"))

def test_length_passengers_for_flight_id_4():
    response = client.get("/flights/4/passengers")
    data = response.json().get("data")
    accounts = get_accounts(4)

    assert len(accounts) == len(data.get("passengers"))

### unique dni ###

def test_unique_passenger_in_airplane_for_flight_id_1():
    response = client.get("/flights/1/passengers")
    passengers = response.json().get("data").get("passengers")

    n = 0
    m = 1
    while n < len(passengers):
        dni = passengers[n].get("dni")
        while m < len(passengers):
            if passengers[m].get("dni") == dni:
                assert False
            m += 1
        n += 1

def test_unique_passenger_in_airplane_for_flight_id_2():
    response = client.get("/flights/2/passengers")
    passengers = response.json().get("data").get("passengers")

    n = 0
    m = 1
    while n < len(passengers):
        dni = passengers[n].get("dni")
        while m < len(passengers):
            if passengers[m].get("dni") == dni:
                assert False
            m += 1
        n += 1

def test_unique_passenger_in_airplane_for_flight_id_3():
    response = client.get("/flights/3/passengers")
    passengers = response.json().get("data").get("passengers")

    n = 0
    m = 1
    while n < len(passengers):
        dni = passengers[n].get("dni")
        while m < len(passengers):
            if passengers[m].get("dni") == dni:
                assert False
            m += 1
        n += 1

def test_unique_passenger_in_airplane_for_flight_id_4():
    response = client.get("/flights/4/passengers")
    passengers = response.json().get("data").get("passengers")

    n = 0
    m = 1
    while n < len(passengers):
        dni = passengers[n].get("dni")
        while m < len(passengers):
            if passengers[m].get("dni") == dni:
                assert False
            m += 1
        n += 1

### seated near passengers with the same purchaseId ###

# def test_80_percent_passengers_seated_near_with_purchase_id_for_flight_id_1():
#     response = client.get("/flights/1/passengers")
#     passengers = response.json().get("data").get("passengers")

#     airplane = get_airplane_data(1).seats
#     purchase_id_for_alone_passengers = get_quantity_passengers_group_by_purchase_id(1)

#     count = 0
#     for passenger in passengers:
#         around_seats = get_around_seats(airplane)
#         if passenger.get("purchaseId") in purchase_id_for_alone_passengers:
#             continue

#         for seat_id in around_seats:
#             for p in passengers:
#                 if p.get("seatId") == seat_id:
#                     if p.get("purchaseId") != passenger.get("purchaseId"):
        

