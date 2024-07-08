# Pydantic
from pydantic import (
    BaseModel,
    Field
)

# models
from models.flight_data import FlightData


class FlightDataResponse(BaseModel):
    code: int = Field(...)
    data: FlightData = Field(...)