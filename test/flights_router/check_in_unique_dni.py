# FastAPI
from fastapi.testclient import TestClient

# main
from main import app


client = TestClient(app)


class TestCheckInUniqueDNI:
    def check_data_for_tests(self, flight_id: int):
        response = client.get(f"/flights/{flight_id}/passengers")
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

    def test_unique_passenger_in_airplane_for_flight_id_1(self):
        self.check_data_for_tests(1)

    def test_unique_passenger_in_airplane_for_flight_id_2(self):
        self.check_data_for_tests(2)

    def test_unique_passenger_in_airplane_for_flight_id_3(self):
        self.check_data_for_tests(3)

    def test_unique_passenger_in_airplane_for_flight_id_4(self):
        self.check_data_for_tests(4)
