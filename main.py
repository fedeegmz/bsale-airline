# Python
import os

# FastAPI
from fastapi import FastAPI, Path
from fastapi import HTTPException, status
# from fastapi.encoders import jsonable_encoder

# mysql
import mysql.connector

# models
from models import FlightData, AirplaneData, ResponseModel

# serializers
from serializers import flight_serializer, airplane_serializer

# util
from util import group_accounts


# load env
db_host = "mdb-test.c6vunyturrl6.us-west-1.rds.amazonaws.com"
db_username = os.getenv("BSALE_AIRLINE_DB_USERNAME")
db_password = os.getenv("BSALE_AIRLINE_DB_PASSWORD")


app = FastAPI()

@app.get("/")
async def root():
    return {"testData": "Hello World"}


@app.get(
    path = "/flights/{flight_id}/passengers",
    status_code = status.HTTP_200_OK,
    # response_model = ResponseModel,
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
                                    f'WHERE s.airplane_id = {flight_data.airplaneId} AND s.seat_id NOT IN ( '\
                                    f'    SELECT bp.seat_id '\
                                    f'    FROM airline.boarding_pass AS bp '\
                                    f'    WHERE bp.seat_id IS NOT NULL AND bp.flight_id = {flight_id});'
        cursor.execute(airplane_data_query)
        airplane_data = cursor.fetchall()
        airplane_data: AirplaneData = airplane_serializer(airplane_data)
        print(airplane_data.dict())

        # get ACCOUNTS
        accounts_data_query: str = f'SELECT bp.boarding_pass_id, bp.purchase_id, bp.seat_type_id, bp.seat_id, '\
                                    f'p.passenger_id, p.dni, p.name, p.age, p.country '\
                                    f'FROM airline.boarding_pass AS bp '\
                                    f'LEFT JOIN airline.passenger AS p '\
                                    f'    ON bp.passenger_id = p.passenger_id '\
                                    f'WHERE flight_id = {flight_id} '\
                                    f'ORDER BY bp.seat_id asc;'
        cursor.execute(accounts_data_query)
        accounts_data = cursor.fetchall()
        accounts_to_update, accounts_ready = group_accounts(accounts_data)

        # TODO: agrupar las cuentas de accounts_to_update e ir agregandolas a accounts_ready


        flight_data.passengers = accounts_ready
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
                "errors": str(err)
            }
        )