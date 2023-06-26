# Pydantic
from pydantic import BaseModel, Field


class AccountData(BaseModel):
    passengerId: int = Field(...)
    dni: int = Field(...)
    name: str = Field(...)
    age: int = Field(...)
    country: str = Field(...)
    boardingPassId: int = Field(...)
    purchaseId: int = Field(...) #FK -> Purchase
    seatTypeId: int = Field(...) #FK -> SeatType
    seatId: int = Field(default=None) #FK -> Seat