# Pydantic
from pydantic import BaseModel, Field


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