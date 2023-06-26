# models
from models.flight_data import FlightData


def flight_serializer(data: tuple):
    dict_to_return = {
        "flightId": int(data[0]),
        "takeoffDateTime": int(data[1]),
        "takeoffAirport": data[2],
        "landingDateTime": int(data[3]),
        "landingAirport": data[4],
        "airplaneId": int(data[5]),
        "passengers": []
    }
    return FlightData(**dict_to_return)