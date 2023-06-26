# Pydantic
from pydantic import BaseModel, Field

# models
from .seat_data import SeatData


class AirplaneData(BaseModel):
    seats: list[SeatData] = Field(...)