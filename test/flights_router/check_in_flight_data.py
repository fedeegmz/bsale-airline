# FastAPI
from fastapi.testclient import TestClient

# main
from main import app

# utils
from utils.get_flight_data import get_flight_data


client = TestClient(app)


class TestCheckInFlightData:
    def check_data_for_tests(self, flight_id: int):
        response = client.get(f"/flights/{flight_id}/passengers")
        data = response.json().get("data")
        flight_data = get_flight_data(flight_id)

        assert data.get("flightId") == flight_data.flight_id
        assert data["takeoffDateTime"] == flight_data.takeoff_date_time
        assert data["takeoffAirport"] == flight_data.takeoff_airport
        assert data["landingDateTime"] == flight_data.landing_date_time
        assert data["landingAirport"] == flight_data.landing_airport
        assert data["airplaneId"] == flight_data.airplane_id

    def test_flight_data_for_flight_id_0(self):
        response = client.get("/flights/0/passengers")
        assert response.json() == {
            "detail": {
                "code": 404,
                "data": {}
            }
        }
    
    def test_flight_data_for_flight_id_1(self):
        self.check_data_for_tests(1)

    def test_flight_data_for_flight_id_2(self):
        self.check_data_for_tests(2)

    def test_flight_data_for_flight_id_3(self):
        self.check_data_for_tests(3)

    def test_flight_data_for_flight_id_4(self):
        self.check_data_for_tests(4)

    def test_flight_data_for_flight_id_5(self):
        response = client.get("/flights/5/passengers")
        assert response.json() == {
            "detail": {
                "code": 404,
                "data": {}
            }
        }
