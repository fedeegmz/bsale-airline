# FastAPI
from fastapi.testclient import TestClient

# main
from main import app


client = TestClient(app)


class TestCheckInUniqueDNI:
    def test_unique_passenger_in_airplane_for_flight_id_1(self):
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

    def test_unique_passenger_in_airplane_for_flight_id_2(self):
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

    def test_unique_passenger_in_airplane_for_flight_id_3(self):
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

    def test_unique_passenger_in_airplane_for_flight_id_4(self):
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
