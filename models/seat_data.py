# Pydantic
from pydantic import BaseModel, Field


class SeatData(BaseModel):
    seatId: int = Field(...)
    seatColumn: str = Field(...)
    seatRow: int = Field(...)
    seatTypeId: int = Field(...) #FK -> SeatType