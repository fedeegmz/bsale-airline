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


class TestCheckInSeatType:
    def test_seated_passengers_in_their_seat_class_for_flight_id_1(self):
        response = client.get("/flights/1/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(1)

        for passenger in passengers:
            seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            if not passenger.get("seatTypeId") == seat.seatTypeId:
                assert False

    def test_seated_passengers_in_their_seat_class_for_flight_id_2(self):
        response = client.get("/flights/2/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(2)

        for passenger in passengers:
            seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            if not passenger.get("seatTypeId") == seat.seatTypeId:
                assert False

    def test_seated_passengers_in_their_seat_class_for_flight_id_3(self):
        response = client.get("/flights/3/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(2)

        for passenger in passengers:
            seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            if not passenger.get("seatTypeId") == seat.seatTypeId:
                assert False

    def test_seated_passengers_in_their_seat_class_for_flight_id_4(self):
        response = client.get("/flights/4/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(1)

        for passenger in passengers:
            seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            if not passenger.get("seatTypeId") == seat.seatTypeId:
                assert False
