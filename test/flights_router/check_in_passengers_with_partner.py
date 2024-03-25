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


class TestCheckInPassengersWithPartner:
    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_1(self):
        response = client.get("/flights/1/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(1)
        purchase_id_for_alone_passengers = get_quantity_passengers_group_by_purchase_id(1)

        passengers_not_alone = 0
        i = 0
        for passenger in passengers:
            if passenger.get("purchaseId") in purchase_id_for_alone_passengers:
                passengers_not_alone += 1

            passenger_seat = search_seat_by_id(passenger.get("seatId"), airplane.seats)
            around_id_seats = get_around_seats(passenger_seat, airplane.seats)
            if not around_id_seats:
                assert False

            n = i + 1
            while n < len(passengers):
                if passenger.get("purchaseId") == passengers[n].get("purchaseId"):
                    for id_seat in around_id_seats:
                        if id_seat == passengers[n].get("seatId"):
                            passengers_not_alone += 1
                            break
                n += 1
            i += 1
        
        assert (100 * passengers_not_alone / len(passengers)) >= 60

    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_2(self):
        response = client.get("/flights/2/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(2)
        purchase_id_for_alone_passengers = get_quantity_passengers_group_by_purchase_id(1)

        passengers_not_alone = 0
        i = 0
        for passenger in passengers:
            if passenger.get("purchaseId") in purchase_id_for_alone_passengers:
                passengers_not_alone += 1

            passenger_seat = search_seat_by_id(passenger.get("seatId"), airplane.seats)
            around_id_seats = get_around_seats(passenger_seat, airplane.seats)
            if not around_id_seats:
                assert False

            n = i + 1
            while n < len(passengers):
                if passenger.get("purchaseId") == passengers[n].get("purchaseId"):
                    for id_seat in around_id_seats:
                        if id_seat == passengers[n].get("seatId"):
                            passengers_not_alone += 1
                            break
                n += 1
            i += 1
        
        assert (100 * passengers_not_alone / len(passengers)) >= 60

    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_3(self):
        response = client.get("/flights/3/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(2)
        purchase_id_for_alone_passengers = get_quantity_passengers_group_by_purchase_id(1)

        passengers_not_alone = 0
        i = 0
        for passenger in passengers:
            if passenger.get("purchaseId") in purchase_id_for_alone_passengers:
                passengers_not_alone += 1

            passenger_seat = search_seat_by_id(passenger.get("seatId"), airplane.seats)
            around_id_seats = get_around_seats(passenger_seat, airplane.seats)
            if not around_id_seats:
                assert False

            n = i + 1
            while n < len(passengers):
                if passenger.get("purchaseId") == passengers[n].get("purchaseId"):
                    for id_seat in around_id_seats:
                        if id_seat == passengers[n].get("seatId"):
                            passengers_not_alone += 1
                            break
                n += 1
            i += 1
        
        assert (100 * passengers_not_alone / len(passengers)) >= 60

    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_4(self):
        response = client.get("/flights/4/passengers")
        passengers = response.json().get("data").get("passengers")
        airplane = get_airplane_data(1)
        purchase_id_for_alone_passengers = get_quantity_passengers_group_by_purchase_id(1)

        passengers_not_alone = 0
        i = 0
        for passenger in passengers:
            if passenger.get("purchaseId") in purchase_id_for_alone_passengers:
                passengers_not_alone += 1

            passenger_seat = search_seat_by_id(passenger.get("seatId"), airplane.seats)
            around_id_seats = get_around_seats(passenger_seat, airplane.seats)
            if not around_id_seats:
                assert False

            n = i + 1
            while n < len(passengers):
                if passenger.get("purchaseId") == passengers[n].get("purchaseId"):
                    for id_seat in around_id_seats:
                        if id_seat == passengers[n].get("seatId"):
                            passengers_not_alone += 1
                            break
                n += 1
            i += 1
        
        assert (100 * passengers_not_alone / len(passengers)) >= 60
