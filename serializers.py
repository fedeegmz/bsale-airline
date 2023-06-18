from models import FlightData, SeatData, AirplaneData


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

def accounts_serializer(data: tuple):
    dict_to_return = {
        "passengerId": int(data[4]),
        "dni": int(data[5]),
        "name": data[6],
        "age": int(data[7]),
        "country": data[8],
        "boardingPassId": int(data[0]),
        "purchaseId": int(data[1]),
        "seatTypeId": int(data[2]),
        "seatId": data[3]
    }
    if data[3]:
        dict_to_return["seatId"] = int(data[3])
    return dict_to_return

def airplane_serializer(data: list):
    list_to_return = []
    for seat in data:
        list_to_return.append(
            SeatData(
                **{
                    "seatId": int(seat[0]),
                    "seatColumn": seat[1],
                    "seatRow": int(seat[2]),
                    "seatTypeId": int(seat[3])
                }
            )
        )
    return AirplaneData(seats=list_to_return)