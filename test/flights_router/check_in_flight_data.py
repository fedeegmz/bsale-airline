# FastAPI
from fastapi.testclient import TestClient

# main
from main import app


client = TestClient(app)


class TestCheckInFlightData:
    def test_flight_data_for_flight_id_0(self):
        response = client.get("/flights/0/passengers")
        assert response.json() == {
            "detail": {
                "code": 404,
                "data": {}
            }
        }
    
    def test_flight_data_for_flight_id_1(self):
        response = client.get("/flights/1/passengers")
        data = response.json().get("data")

        assert data.get("flightId") == 1
        assert data["takeoffDateTime"] == 1688207580
        assert data["takeoffAirport"] == "Aeropuerto Internacional Arturo Merino Benitez, Chile"
        assert data["landingDateTime"] == 1688221980
        assert data["landingAirport"] == "Aeropuerto Internacional Jorge Cháve, Perú"
        assert data["airplaneId"] == 1

    def test_flight_data_for_flight_id_2(self):
        response = client.get("/flights/2/passengers")
        data = response.json().get("data")

        assert data.get("flightId") == 2
        assert data.get("takeoffDateTime") == 1688491980
        assert data.get("takeoffAirport") == "Aeropuerto Internacional Jorge Cháve, Perú"
        assert data.get("landingDateTime") == 1688495580
        assert data.get("landingAirport") == "Aeropuerto Francisco Carlé, Perú"
        assert data.get("airplaneId") == 2

    def test_flight_data_for_flight_id_3(self):
        response = client.get("/flights/3/passengers")
        data = response.json().get("data")

        assert data.get("flightId") == 3
        assert data.get("takeoffDateTime") == 1688766182
        assert data.get("takeoffAirport") == "Aeropuerto El Tepual, Chile"
        assert data.get("landingDateTime") == 1688772962
        assert data.get("landingAirport") == "Aeropuerto Internacional Arturo Merino Benitez, Chile"
        assert data.get("airplaneId") == 2

    def test_flight_data_for_flight_id_4(self):
        response = client.get("/flights/4/passengers")
        data = response.json().get("data")

        assert data.get("flightId") == 4
        assert data.get("takeoffDateTime") == 1689786902
        assert data.get("takeoffAirport") == "Aeropuerto Internacional Arturo Merino Benitez, Chile"
        assert data.get("landingDateTime") == 1689819302
        assert data.get("landingAirport") == "Aeropuerto Internacional de la Ciudad de México, México"
        assert data.get("airplaneId") == 1

    def test_flight_data_for_flight_id_5(self):
        response = client.get("/flights/5/passengers")
        assert response.json() == {
            "detail": {
                "code": 404,
                "data": {}
            }
        }
