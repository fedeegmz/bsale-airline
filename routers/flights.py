# Python
from datetime import date, datetime

# FastAPI
from fastapi import APIRouter, Path
from fastapi import HTTPException, status

# SQLAlchemy
from sqlalchemy import select

# database
from database.mysql_client import conn

# data_structures
from data_structures.queue import Queue

# schemas
from schemas.flight import FlightTable
from schemas.seat import SeatTable
from schemas.boarding_pass import BoardingPassTable
from schemas.passenger import PassengerTable

# models
from models.flight_data import FlightData
from models.airplane_data import AirplaneData
from models.seat_data import SeatData
from models.passenger_data import PassengerData
from models.response.flight_data_response import FlightDataResponse

# util
from util.white_lists import get_flights_id_in_db
from util.util import order_ready_passengers


router = APIRouter(
    prefix = "/flights"
)

### PATH OPERATIONS ###

@router.get(
    path = "/{flight_id}/passengers",
    status_code = status.HTTP_200_OK,
    response_model = FlightDataResponse,
    summary = "Returns the check-in data",
    tags = ["check-in"]
)
async def check_in(
    flight_id: int = Path(...)
):
    if not flight_id in get_flights_id_in_db():
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = {
                "code": 404,
                "data": {}
            }
        )

    flight_data_result = conn.execute(
        select(
            FlightTable
        ).where(
            FlightTable.c.flight_id == flight_id
        )
    ).first()
    flight_data = FlightData(*flight_data_result)
    del flight_data_result

    print(f"Getting data for:")
    print(f"  FLIGHT: {flight_data.flight_id}")
    print(f"  AIRPLANE: {flight_data.airplane_id}")
    print(f"  FROM: {flight_data.takeoff_airport}")
    print(f"    AT: {datetime.fromtimestamp(flight_data.takeoff_date_time)}")
    print(f"  TO: {flight_data.landing_airport}")
    print(f"    AT: {datetime.fromtimestamp(flight_data.landing_date_time)}\n")

    airplane_result = conn.execute(
        select(
            SeatTable
        ).where(
            SeatTable.c.airplane_id == flight_data.airplane_id
        ).order_by(
            SeatTable.c.seat_column,
            SeatTable.c.seat_row
        )
    ).all()
    airplane = AirplaneData(
        seats = [SeatData(*item) for item in airplane_result]
    )
    del airplane_result

    passengers_result = conn.execute(
        select(PassengerTable, BoardingPassTable).join(
            BoardingPassTable,
            PassengerTable.c.passenger_id == BoardingPassTable.c.passenger_id
        ).where(
            BoardingPassTable.c.flight_id == flight_data.flight_id
        ).order_by(
            BoardingPassTable.c.purchase_id,
            BoardingPassTable.c.seat_type_id,
            BoardingPassTable.c.seat_id.desc(), # DESC
            PassengerTable.c.age
        )
    ).all()
    passengers = [PassengerData(*passenger) for passenger in passengers_result]
    del passengers_result

    assert airplane.update_seats(passengers) #-> updated airplane with seated passengers
    
    ## TODO --> order passengers list by:
    ##              - group of passengers with equal purchase_id and a child
    ##              - greather group of passengers first

    passengers_queue = Queue()
    passengers_queue.enqueue_list(passengers)
    grouped_passengers_queue = Queue()
    ready_passengers: list[PassengerData] = []
    print(f"{len(passengers)} passengers on flight.")
    print(f"{len(airplane.seats)} seats on airplane.\n")

    assert passengers_queue.size() <= len(airplane.seats), f"There are {passengers_queue.size()} passengers in the queue"
    
    while passengers_queue.size() > 0:
        
        if grouped_passengers_queue.size() == 0:
            grouped_passengers_queue.enqueue(passengers_queue.dequeue())
            continue
        
        head = passengers_queue.dequeue()
        new_head_data = grouped_passengers_queue.head.get_data()
        if head.purchase_id == new_head_data.purchase_id and head.seat_type_id == new_head_data.seat_type_id:
            grouped_passengers_queue.enqueue(head)
            continue
        ## grouped passengers by purchase_id and seat_type_id
        
        while grouped_passengers_queue.size() > 0:
            first_passenger = grouped_passengers_queue.head.get_data()
            
            if first_passenger.seat_id:
                ready_passengers.append(first_passenger.model_copy())
                first_passenger = grouped_passengers_queue.dequeue()
                if not grouped_passengers_queue.head:
                    break

                second_passenger = grouped_passengers_queue.head.get_data()
                if second_passenger.seat_id:
                    continue
                near_seat_to_asign = airplane.get_near_seat(first_passenger.seat_id)
                if not near_seat_to_asign:
                    continue

                second_passenger.seat_id = near_seat_to_asign.seat_id
                grouped_passengers_queue.head.set_data(
                    second_passenger
                )
                airplane.update_passenger_id(
                    near_seat_to_asign.seat_id,
                    grouped_passengers_queue.head.get_data().passenger_id
                )
            
            else: #--> first_passenger.seat_id is None
                new_passenger_data = first_passenger.model_copy()
                quantity_seats_to_search = grouped_passengers_queue.size()

                available_seat = airplane.search_group_of_available_seats(
                    seat_type = new_passenger_data.seat_type_id,
                    quantity = quantity_seats_to_search
                )
                while not available_seat:
                    quantity_seats_to_search -= 1
                    available_seat = airplane.search_group_of_available_seats(
                        seat_type = new_passenger_data.seat_type_id,
                        quantity = quantity_seats_to_search
                    )
                new_passenger_data.seat_id = available_seat.seat_id
                grouped_passengers_queue.head.set_data(
                    new_passenger_data
                )
                airplane.update_passenger_id(
                    new_passenger_data.seat_id,
                    new_passenger_data.passenger_id
                )

        grouped_passengers_queue.clear()
        grouped_passengers_queue.enqueue(head)
    
    flight_data.passengers = order_ready_passengers(ready_passengers)
    response = FlightDataResponse(
        code = status.HTTP_200_OK,
        data = flight_data
    )

    print(f"Ready passengers: {len(ready_passengers)}")
    
    return response
