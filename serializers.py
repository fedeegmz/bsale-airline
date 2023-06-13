from models import FlightData, SeatData, AirplaneData


def flight_serializer(data: tuple):
    dict_to_return = {
        "flightId": data[0],
        "takeoffDateTime": data[1],
        "takeoffAirport": data[2],
        "landingDateTime": data[3],
        "landingAirport": data[4],
        "airplaneId": data[5],
        "passengers": []
    }
    return FlightData(**dict_to_return)

def accounts_serializer(data: tuple):
    dict_to_return = {
        "passengerId": data[4],
        "dni": data[5],
        "name": data[6],
        "age": data[7],
        "country": data[8],
        "boardingPassId": data[0],
        "purchaseId": data[1],
        "seatTypeId": data[2],
        "seatId": data[3]
    }
    return dict_to_return

def airplane_serializer(data: list):
    list_to_return = []
    for seat in data:
        list_to_return.append(
            SeatData(
                **{
                    "seatId": seat[0],
                    "seatColumn": seat[1],
                    "seatRow": seat[2],
                    "seatTypeId": seat[3]
                }
            )
        )
    return AirplaneData(seats=list_to_return)