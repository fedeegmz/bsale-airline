# Python
import os

# FastAPI
from fastapi.testclient import TestClient

# MySQL
import mysql.connector

# main
from main import app

# models
from models.seat_data import SeatData
from models.airplane_data import AirplaneData


client = TestClient(app)


class TestCheckInLengthPassengers:
    def test_length_passengers_for_flight_id_1(self):
        response = client.get("/flights/1/passengers")
        data = response.json().get("data")
        accounts = get_accounts(1)

        assert len(accounts) == len(data.get("passengers"))

    def test_length_passengers_for_flight_id_2(self):
        response = client.get("/flights/2/passengers")
        data = response.json().get("data")
        accounts = get_accounts(2)

        assert len(accounts) == len(data.get("passengers"))

    def test_length_passengers_for_flight_id_3(self):
        response = client.get("/flights/3/passengers")
        data = response.json().get("data")
        accounts = get_accounts(3)

        assert len(accounts) == len(data.get("passengers"))

    def test_length_passengers_for_flight_id_4(self):
        response = client.get("/flights/4/passengers")
        data = response.json().get("data")
        accounts = get_accounts(4)

        assert len(accounts) == len(data.get("passengers"))
