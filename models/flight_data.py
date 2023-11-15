# Pydantic
from pydantic import BaseModel, Field, ConfigDict
from pydantic.alias_generators import to_camel

# models
from models.passenger_data import PassengerData


class FlightData(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)
    
    flight_id: int = Field(...)
    takeoff_date_time: int = Field(...)
    takeoff_airport: str = Field(...)
    landing_date_time: int = Field(...)
    landing_airport: str = Field(...)
    airplane_id: int = Field(...)
    passengers: list[PassengerData] = Field(default = [])

    def __init__(self, *args):
        assert len(args) >= 6

        dict_args = {
            "flightId": args[0],
            "takeoffDateTime": args[1],
            "takeoffAirport": args[2],
            "landingDateTime": args[3],
            "landingAirport": args[4],
            "airplaneId": args[5]
        }
        if len(args) == 7:
            dict_args.update({"passengers": args[6]})
        
        super().__init__(**dict_args)
