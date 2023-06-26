# Pydantic
from pydantic import BaseModel, Field

# models
from .account_data import AccountData


class FlightData(BaseModel):
    flightId: int = Field(...)
    takeoffDateTime: int = Field(...)
    takeoffAirport: str = Field(...)
    landingDateTime: int = Field(...)
    landingAirport: str = Field(...)
    airplaneId: int = Field(...) #FK -> Airplane
    passengers: list[AccountData] = Field(default=[])