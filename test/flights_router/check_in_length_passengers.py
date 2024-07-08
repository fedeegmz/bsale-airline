# FastAPI
from fastapi.testclient import TestClient

# main
from main import app

# utils
from utils.get_passengers_data import get_passengers_data


client = TestClient(app)


class TestCheckInLengthPassengers:
    def check_data_for_tests(self, flight_id: int):
        response = client.get(f"/flights/{flight_id}/passengers")
        data = response.json().get("data")
        passengers = get_passengers_data(flight_id)

        assert len(passengers) == len(data.get("passengers"))
    
    def test_length_passengers_for_flight_id_1(self):
        self.check_data_for_tests(1)

    def test_length_passengers_for_flight_id_2(self):
        self.check_data_for_tests(2)

    def test_length_passengers_for_flight_id_3(self):
        self.check_data_for_tests(3)

    def test_length_passengers_for_flight_id_4(self):
        self.check_data_for_tests(4)
