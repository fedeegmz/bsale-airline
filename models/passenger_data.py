# Pydantic
from pydantic import (
    BaseModel,
    Field,
    ConfigDict
)
from pydantic.alias_generators import to_camel


class PassengerData(BaseModel):
    model_config = ConfigDict(
        alias_generator = to_camel
    )
    
    passenger_id: int = Field(...)
    dni: int = Field(...)
    name: str = Field(...)
    age: int = Field(...)
    country: str = Field(...)
    boarding_pass_id: int = Field(...)
    purchase_id: int = Field(...)
    seat_type_id: int = Field(...)
    seat_id: int | None = Field(
        default = None
    )

    def __init__(self, *args, **dict_args):
        if args:
            assert len(args) >= 8
            
            dict_args = {
                "passengerId": args[0],
                "dni": args[1],
                "name": args[2],
                "age": args[3],
                "country": args[4],
                "boardingPassId": args[5],
                "purchaseId": args[6],
                "seatTypeId": args[8],
                "seatId": args[9]
            }
        
        super().__init__(**dict_args)
