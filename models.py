# Pydantic
from pydantic import BaseModel, Field

class AccountData(BaseModel):
    passengerId: int = Field(...)
    dni: str = Field(...)
    name: str = Field(...)
    age: int = Field(...)
    country: str = Field(...)
    boardingPassId: int = Field(...)
    purchaseId: int = Field(...) #FK -> Purchase
    seatTypeId: int = Field(...) #FK -> SeatType
    seatId: int = Field(default=None) #FK -> Seat

class FlightData(BaseModel):
    flightId: int = Field(...)
    takeoffDateTime: int = Field(...)
    takeoffAirport: str = Field(...)
    landingDateTime: int = Field(...)
    landingAirport: str = Field(...)
    airplaneId: int = Field(...) #FK -> Airplane
    passengers: list[AccountData] = Field(default=[])

class SeatData(BaseModel):
    seatId: int = Field(...)
    seatColumn: str = Field(...)
    seatRow: str = Field(...)
    seatTypeId: int = Field(...) #FK -> SeatType

class AirplaneData(BaseModel):
    seats: list[SeatData] = Field(...)

class Flight(BaseModel):
    flightId: int = Field(...)
    takeoffDateTime: int = Field(...)
    takeoffAirport: str = Field(...)
    landingDateTime: int = Field(...)
    landingAirport: str = Field(...)
    airplaneId: int = Field(...) #FK -> Airplane

class BoardingPass(BaseModel):
    boardingPassId: int = Field(...)
    purchaseId: int = Field(...) #FK -> Purchase
    passengerId: int = Field(...) #FK -> Passenger
    seatTypeId: int = Field(...) #FK -> SeatType
    seatId: int = Field(default=None) #FK -> Seat
    flightId: int = Field(...) #FK -> Flight

class Purchase(BaseModel):
    purchaseId: int = Field(...)
    purchaseDate: int = Field(...)

class Passenger(BaseModel):
    passengerId: int = Field(...)
    dni: str = Field(...)
    name: str = Field(...)
    age: int = Field(...)
    country: str = Field(...)

class Seat(BaseModel):
    seatId: int = Field(...)
    seatColumn: str = Field(...)
    seatRow: str = Field(...)
    seatTypeId: int = Field(...) #FK -> SeatType
    airplaneId: int = Field(...) #FK -> Airplane

class SeatType(BaseModel):
    seatTypeId: int = Field(...)
    name: str = Field(...)

class Airplane(BaseModel):
    airplaneId: int = Field(...)
    name: str = Field(...)



### RESPONSE ###
class ResponsePassengers(BaseModel):
    passengerId: int = Field(...)
    dni: int = Field(...)
    name: str = Field(...)
    age: int = Field(...)
    country: str = Field(...)
    boardingPassId: int = Field(...)
    purchaseId: int = Field(...)
    seatTypeId: int = Field(...)
    seatId: int = Field(...)

class ResponseData(BaseModel):
    flightId: int = Field(...)
    takeoffDateTime: int = Field(...)
    takeoffAirport: str = Field(...)
    landingDateTime: int = Field(...)
    landingAirport: str = Field(...)
    airplaneId: int = Field(...)
    passengers: list[ResponsePassengers] = Field(...)

class ResponseModel(BaseModel):
    code: int = Field(...)
    data: ResponseData = Field(...)