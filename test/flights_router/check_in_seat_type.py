# FastAPI
from fastapi.testclient import TestClient

# main
from main import app

# utils
from utils.get_airplane_data import get_airplane_data


client = TestClient(app)


class TestCheckInSeatType:
    def check_data_for_tests(self, flight_id: int):
        response = client.get(f"/flights/{flight_id}/passengers")
        data = response.json().get("data")
        passengers = data.get("passengers")
        airplane = get_airplane_data(
            data.get("airplaneId")
        )

        for passenger in passengers:
            seat = airplane.search_seat_by_id(
                passenger.get("seatId")
            )
            if not passenger.get("seatTypeId") == seat.seat_type_id:
                assert False

    def test_seated_passengers_in_their_seat_class_for_flight_id_1(self):
        self.check_data_for_tests(1)

    def test_seated_passengers_in_their_seat_class_for_flight_id_2(self):
        self.check_data_for_tests(2)

    def test_seated_passengers_in_their_seat_class_for_flight_id_3(self):
        self.check_data_for_tests(3)

    def test_seated_passengers_in_their_seat_class_for_flight_id_4(self):
        self.check_data_for_tests(4)
