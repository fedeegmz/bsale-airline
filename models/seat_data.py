# Pydantic
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel


class SeatData(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    seat_id: int = Field(...)
    seat_column: str = Field(...)
    seat_row: int = Field(...)
    seat_type_id: int = Field(...)

    def __init__(self, *args):
        assert len(args) == 4

        dict_args = {
            "seatId": args[0],
            "seatColumn": args[1],
            "seatRow": args[2],
            "seatTypeId": args[3]
        }
        
        super().__init__(**dict_args)
