# FastAPI
from fastapi.testclient import TestClient

# main
from main import app

# models
from models.passenger_data import PassengerData

# utils
from utils.get_airplane_data import get_airplane_data


client = TestClient(app)


class TestCheckInChildrenWithParent:
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
        
        for passenger in passengers:
            if passenger.age >= 18:
                continue
            
            left_seat, right_seat = airplane.get_left_right_seats(
                seat_id = passenger.seat_id,
                empty_seat = False
            )
            
            purchase_id_left_passenger = None
            purchase_id_right_passenger = None
            
            for p in passengers:
                if left_seat and p.seat_id == left_seat.seat_id:
                    purchase_id_left_passenger = p.purchase_id
                if right_seat and p.seat_id == right_seat.seat_id:
                    purchase_id_right_passenger = p.purchase_id
            
            assert passenger.purchase_id == purchase_id_left_passenger or passenger.purchase_id == purchase_id_right_passenger
    
    def test_children_seated_with_parent_for_flight_id_1(self):
        self.check_data_for_tests(1)

    def test_children_seated_with_parent_for_flight_id_2(self):
        self.check_data_for_tests(2)
    
    def test_children_seated_with_parent_for_flight_id_3(self):
        self.check_data_for_tests(3)
    
    def test_children_seated_with_parent_for_flight_id_4(self):
        self.check_data_for_tests(4)
