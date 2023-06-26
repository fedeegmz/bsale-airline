# Pydantic
from pydantic import BaseModel, Field



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
