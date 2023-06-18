# Python
import os

# FastAPI
from fastapi import FastAPI, Path
from fastapi import HTTPException, status

# mysql
import mysql.connector

# models
from models import FlightData, AirplaneData, SeatData, AccountData, ResponseModel

# serializers
from serializers import flight_serializer, airplane_serializer, accounts_serializer

# util
from util import group_accounts, get_parents, get_near_seat
from util import search_seat_by_id, search_seat_for_two_passengers, search_group_of_empty_seats
from util import update_airplane, assign_seat_for_passenger, order_ready_accounts

# load env
db_host = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
db_username = os.getenv("BSALE_AIRLINE_DB_USERNAME")
db_password = os.getenv("BSALE_AIRLINE_DB_PASSWORD")


app = FastAPI()

@app.get("/")
async def root():
    return {"url": "https://checkinairline-1-s8126205.deta.app/flights/1/passengers"}


@app.get(
    path = "/flights/{flight_id}/passengers",
    status_code = status.HTTP_200_OK,
    response_model = ResponseModel,
    summary = "Returns the check-in data",
    tags = ["check-in"]
)
async def check_in(
    flight_id: str = Path(...)
):
    try:
        ### db connection ###
        cnx = mysql.connector.connect(
            host = db_host,
            user = db_username,
            password = db_password,
            database = "airline"
        )
        cursor = cnx.cursor()

    except:
        raise HTTPException(
            status_code = status.HTTP_400_BAD_REQUEST,
            detail = {
                "code": 400,
                "errors": "could not connect to db"
            }
        )

    try:
        # get FLIGHT DATA
        flight_data_query: str = f'SELECT * FROM flight WHERE flight_id = {flight_id}'
        cursor.execute(flight_data_query)
        flight_data = cursor.fetchone()
        flight_data: FlightData = flight_serializer(flight_data)

        # get AIRPLANE DATA (empty seats)
        airplane_data_query: str = f'SELECT s.seat_id, s.seat_column, s.seat_row, s.seat_type_id '\
                                    f'FROM airline.seat AS s '\
                                    f'WHERE s.airplane_id = {flight_data.airplaneId}'
        airplane_empty_seats_query: str = f'SELECT s.seat_id, s.seat_column, s.seat_row, s.seat_type_id '\
                                    f'FROM airline.seat AS s '\
                                    f'WHERE s.airplane_id = {flight_data.airplaneId} AND s.seat_id NOT IN ( '\
                                    f'    SELECT bp.seat_id '\
                                    f'    FROM airline.boarding_pass AS bp '\
                                    f'    WHERE bp.seat_id IS NOT NULL AND bp.flight_id = {flight_id});'
        cursor.execute(airplane_data_query)
        airplane_data = cursor.fetchall()
        cursor.execute(airplane_empty_seats_query)
        airplane_empty_seats = cursor.fetchall()
        airplane_data: AirplaneData = airplane_serializer(airplane_data)
        airplane_empty_seats: AirplaneData = airplane_serializer(airplane_empty_seats)

        # get ACCOUNTS
        accounts_data_query: str = f'SELECT bp.boarding_pass_id, bp.purchase_id, bp.seat_type_id, bp.seat_id, '\
                                    f'p.passenger_id, p.dni, p.name, p.age, p.country '\
                                    f'FROM airline.boarding_pass AS bp '\
                                    f'LEFT JOIN airline.passenger AS p '\
                                    f'    ON bp.passenger_id = p.passenger_id '\
                                    f'left join ( '\
                                    f'  SELECT COUNT(*) AS quantity, purchase_id '\
                                    f'  FROM airline.boarding_pass '\
                                    f'  WHERE flight_id = {flight_id} '\
                                    f'  GROUP BY purchase_id '\
                                    f'  ORDER BY quantity DESC '\
                                    f') AS q '\
                                    f'  ON bp.purchase_id = q.purchase_id '\
                                    f'WHERE flight_id = {flight_id} '\
                                    f'ORDER BY q.quantity DESC, bp.purchase_id;'
        cursor.execute(accounts_data_query)
        accounts_data = cursor.fetchall() # accounts ordenadas por cantidad de compra
        accounts_data: list[AccountData] = [AccountData(**accounts_serializer(account)) for account in accounts_data]

        parents: list[AccountData]
        accounts_to_update, accounts_ready, children = group_accounts(accounts_data)
        print(f'accounts: {len(children) + len(accounts_ready) + len(accounts_to_update)}')

        # seat children and parents
        # TODO: si es posible, asignar asientos todos en la misma fila
        for child in children:
            parents: list[AccountData] = get_parents(child, accounts_to_update, accounts_ready)

            if len(children) != 0 and not parents:
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = {
                        "code": 409,
                        "errors": "There is a child alone"
                    }
                )
            
            for parent in parents:
                if not child.seatId:
                    child_seat, parent_seat = search_seat_for_two_passengers(
                        child.seatTypeId,
                        airplane_empty_seats.seats,
                        flight_data.airplaneId,
                        True
                    )
                    if not child_seat or not parent_seat:
                        raise HTTPException(
                            status_code = status.HTTP_409_CONFLICT,
                            detail = {
                                "code": 409,
                                "errors": "Seat not found"
                            }
                        )
                    
                    child.seatId = child_seat
                    parent.seatId = parent_seat
                    update_airplane(child_seat, airplane_empty_seats.seats)
                    update_airplane(parent_seat, airplane_empty_seats.seats)

                elif child.seatId:
                    parent_seat = get_near_seat(
                        search_seat_by_id(child.seatId, airplane_data.seats),
                        airplane_empty_seats.seats
                    )
                    
                    if parent_seat:
                        parent.seatId = parent_seat.seatId
                        update_airplane(parent_seat.seatId, airplane_empty_seats.seats)
                if parent.seatId:
                    assign_seat_for_passenger(
                        passenger = parent,
                        passengers_list = accounts_ready
                    )
                else:
                    accounts_to_update.append(parent)

            if not child.seatId:
                raise HTTPException(
                    status_code = status.HTTP_409_CONFLICT,
                    detail = {
                        "code": 409,
                        "errors": "Seat not found"
                    }
                )
            assign_seat_for_passenger(
                passenger = child,
                passengers_list = accounts_ready
            )
        
        # seat people group by purchaseId
        group_accounts_by_purchase_id: list[list[AccountData]] = [] # lista con listas de cuentas agrupadas por purchaseId
        accounts_group: list[AccountData] = []
        m = 0
        for account in accounts_to_update:
            
            if len(accounts_group) == 0:
                accounts_group.append(account)
            elif account.purchaseId == accounts_group[len(accounts_group) - 1].purchaseId:
                accounts_group.append(account)
            elif not account.purchaseId == accounts_group[len(accounts_group) - 1].purchaseId:
                    
                group_accounts_by_purchase_id.append(accounts_group)
                accounts_group = []
                accounts_group.append(account)
                if m == len(accounts_to_update):
                    group_accounts_by_purchase_id.append(accounts_group)
            m += 1
        
        for accounts in group_accounts_by_purchase_id:
            group_available_seats: list[list] = search_group_of_empty_seats(
                accounts[0].seatTypeId,
                airplane_empty_seats.seats
            )
            
            for group in group_available_seats:
                if len(group) >= len(accounts):

                    for account in accounts:
                        seat_id = group.pop()
                        seat_to_assign = search_seat_by_id(seat_id, airplane_empty_seats.seats)
                        if seat_to_assign and account.seatTypeId == seat_to_assign.seatTypeId and account.seatId == None:
                            assign_seat_for_passenger(
                                seat_id = seat_id,
                                passenger = account,
                                passengers_list = accounts_ready,
                                airplane = airplane_empty_seats.seats
                            )
                            n = 0
                            for p in accounts_to_update:
                                if account.dni == p.dni:
                                    accounts_to_update.pop(n)
                                n += 1
        
        if len(accounts_to_update) != 0:
            for acc in accounts_to_update:
                for seat in airplane_empty_seats.seats:
                    if not acc.seatId and seat.seatTypeId == acc.seatTypeId:
                        assign_seat_for_passenger(
                            seat_id = seat.seatId,
                            passenger = acc,
                            passengers_list = accounts_ready,
                            airplane = airplane_empty_seats.seats
                        )
        
        print(f'to_update_after_assignament: {len(accounts_to_update)}')
        print([(a.purchaseId, a.seatId) for a in accounts_to_update])

        flight_data.passengers = order_ready_accounts(accounts_ready)
        print(f'ready: {len(flight_data.passengers)}')
        return ResponseModel(
            code = 200,
            data = flight_data.dict()
        ).dict()
    
    except Exception as err:
        raise HTTPException(
            status_code = status.HTTP_404_NOT_FOUND,
            detail = {
                "code": 404,
                "data": {},
                # "errmsg": str(err)
            }
        )