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


class TestCheckInChildrenWithParent:
    def test_children_seated_with_parent_for_flight_id_1(self):
        response = client.get("/flights/1/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(1)

        parent_seated_next_to = False
        for passenger in passengers:
            if passenger.get("age") > 18:
                continue

            child_seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            next_to_seats = get_next_to(
                child_seat,
                airplane.seats
            )
            if not next_to_seats:
                assert parent_seated_next_to

            for p in passengers:
                if passenger.get("dni") == p.get("dni"):
                    continue
                if not passenger.get("purchaseId") == p.get("purchaseId"):
                    continue

                for seat in next_to_seats:
                    if seat.seatId == p.get("seatId"):
                        parent_seated_next_to = True
        
        assert parent_seated_next_to

    def test_children_seated_with_parent_for_flight_id_2(self):
        response = client.get("/flights/2/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(2)

        parent_seated_next_to = False
        for passenger in passengers:
            if passenger.get("age") > 18:
                continue

            child_seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            next_to_seats = get_next_to(
                child_seat,
                airplane.seats
            )
            if not next_to_seats:
                assert parent_seated_next_to

            for p in passengers:
                if passenger.get("dni") == p.get("dni"):
                    continue
                if not passenger.get("purchaseId") == p.get("purchaseId"):
                    continue

                for seat in next_to_seats:
                    if seat.seatId == p.get("seatId"):
                        parent_seated_next_to = True
        
        assert parent_seated_next_to

    def test_children_seated_with_parent_for_flight_id_3(self):
        response = client.get("/flights/3/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(2)

        parent_seated_next_to = False
        for passenger in passengers:
            if passenger.get("age") > 18:
                continue

            child_seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            next_to_seats = get_next_to(
                child_seat,
                airplane.seats
            )
            if not next_to_seats:
                assert parent_seated_next_to

            for p in passengers:
                if passenger.get("dni") == p.get("dni"):
                    continue
                if not passenger.get("purchaseId") == p.get("purchaseId"):
                    continue

                for seat in next_to_seats:
                    if seat.seatId == p.get("seatId"):
                        parent_seated_next_to = True
        
        assert parent_seated_next_to

    def test_children_seated_with_parent_for_flight_id_4(self):
        response = client.get("/flights/4/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(1)

        parent_seated_next_to = False
        for passenger in passengers:
            if passenger.get("age") > 18:
                continue

            child_seat = search_seat_by_id(
                passenger.get("seatId"),
                airplane.seats
            )
            next_to_seats = get_next_to(
                child_seat,
                airplane.seats
            )
            if not next_to_seats:
                assert parent_seated_next_to

            for p in passengers:
                if passenger.get("dni") == p.get("dni"):
                    continue
                if not passenger.get("purchaseId") == p.get("purchaseId"):
                    continue

                for seat in next_to_seats:
                    if seat.seatId == p.get("seatId"):
                        parent_seated_next_to = True
        
        assert parent_seated_next_to
