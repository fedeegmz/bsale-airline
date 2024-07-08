# FastAPI
from fastapi.testclient import TestClient

# main
from main import app

# models
from models.passenger_data import PassengerData

# utils
from utils.get_airplane_data import get_airplane_data
from utils.get_around_seats import get_around_seats
from utils.get_q_passengers_group_by_purchase_id import (
    get_q_passengers_group_by_purchase_id
)


client = TestClient(app)


class TestCheckInPassengersWithPartner:
    def check_data_for_tests(self, flight_id: int):
        response = client.get(f"/flights/{flight_id}/passengers")
        data = response.json().get("data")
        passengers = [
            PassengerData(**item)
            for item in data.get("passengers")
        ]
        airplane = get_airplane_data(
            data.get("airplaneId")
        )
        purchase_id_for_alone_passengers = get_q_passengers_group_by_purchase_id(
            flight_id
        )
        
        passengers_not_alone = 0
        i = 0
        for passenger in passengers:
            if passenger.purchase_id in purchase_id_for_alone_passengers:
                passengers_not_alone += 1

            around_id_seats = get_around_seats(
                passenger.seat_id,
                airplane
            )
            if not around_id_seats:
                assert False

            n = i + 1
            while n < len(passengers):
                if passenger.purchase_id == passengers[n].purchase_id:
                    for id_seat in around_id_seats:
                        if id_seat == passengers[n].seat_id:
                            passengers_not_alone += 1
                            break
                n += 1
            i += 1
        
        assert (100 * passengers_not_alone / len(passengers)) >= 65

    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_1(self):
        self.check_data_for_tests(1)

    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_2(self):
        self.check_data_for_tests(2)

    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_3(self):
        self.check_data_for_tests(3)

    def test_60_percent_passengers_seated_near_with_purchase_id_for_flight_id_4(self):
        self.check_data_for_tests(4)
