import os
from fastapi.testclient import TestClient
import mysql.connector

from main import app
from models import AccountData
from serializers import accounts_serializer

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

