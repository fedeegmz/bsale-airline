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