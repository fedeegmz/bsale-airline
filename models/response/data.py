# Pydantic
from pydantic import BaseModel, Field

# models
from models.response.passengers import ResponsePassengers


class ResponseData(BaseModel):
    flightId: int = Field(...)
    takeoffDateTime: int = Field(...)
    takeoffAirport: str = Field(...)
    landingDateTime: int = Field(...)
    landingAirport: str = Field(...)
    airplaneId: int = Field(...)
    passengers: list[ResponsePassengers] = Field(...)