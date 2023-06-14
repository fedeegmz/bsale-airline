from models import AccountData, SeatData, AirplaneData

def group_accounts(accounts: list):
    """
    Agrupa los pasajeros que tiene asientos y los que no
    Params:
        - accounts
    Returns:
        - accounts_to_update: list[AccountData]
        - accounts_ready: list[AccountData]
    """
    accounts_to_update: list[AccountData] = []
    accounts_ready: list[AccountData] = []
    for account in accounts:
        if account.seatId == None:
            accounts_to_update.append(account)
        else:
            accounts_ready.append(account)

    return (accounts_to_update, accounts_ready)

def group_children(accounts: list[AccountData]):
    """
    Agrupa las personas menores de 18 años
    Params:
        - accounts
    Returns:
        - list[AccountData]
    """
    list_to_return = []
    n = 0
    for account in accounts:
        if account.age < 18:
            list_to_return.append(account)
            del accounts[n]
        n += 1
    return list_to_return

def get_parents(child: AccountData, accounts: list[AccountData]):
    """
    Busca pasajeros con igual purchaseId
    Params:
        - child
        - accounts
    Returns:
        - list[AccountData]
    """
    list_to_return: list = []
    n = 0
    for account in accounts:
        if child.purchaseId == account.purchaseId:
            list_to_return.append(account)
            del accounts[n]
    
    if len(list_to_return) == 0:
        return None
    
    return list_to_return

def get_next_to(seat: SeatData, airplane: AirplaneData, airplane_type: int):
    """
    Busca un asiento consecutivo y disponible
    Params:
        - seat
        - airplane
        - airplane_type
    Returns:
        - SeatData
    """
    if airplane_type == 1:
        if seat.seatTypeId == 1:
            if seat.seatColumn == "A":
                return _search_next_to_in_airplane("B", seat.seatRow, airplane.seats)
            if seat.seatColumn == "B":
                return _search_next_to_in_airplane("A", seat.seatRow, airplane.seats)
            if seat.seatColumn == "F":
                return _search_next_to_in_airplane("G", seat.seatRow, airplane.seats)
            if seat.seatColumn == "G":
                return _search_next_to_in_airplane("F", seat.seatRow, airplane.seats)
        else:
            if seat.seatColumn == "A":
                return _search_next_to_in_airplane("B", seat.seatRow, airplane.seats)
            if seat.seatColumn == "B":
                available_seats = _search_next_to_in_airplane("A", seat.seatRow, airplane.seats)
                if not available_seats:
                    available_seats = _search_next_to_in_airplane("C", seat.seatRow, airplane.seats)
                return available_seats
            if seat.seatColumn == "C":
                return _search_next_to_in_airplane("B", seat.seatRow, airplane.seats)
            
            if seat.seatColumn == "E":
                return _search_next_to_in_airplane("F", seat.seatRow, airplane.seats)
            if seat.seatColumn == "F":
                available_seats = _search_next_to_in_airplane("E", seat.seatRow, airplane.seats)
                if not available_seats:
                    available_seats = _search_next_to_in_airplane("G", seat.seatRow, airplane.seats)
                return available_seats
            if seat.seatColumn == "G":
                return _search_next_to_in_airplane("F", seat.seatRow, airplane.seats)
    elif airplane_type == 2:
        if seat.seatTypeId == 1:
            return None
        else:
            if seat.seatColumn == "A":
                return _search_next_to_in_airplane("B", seat.seatRow, airplane.seats)
            if seat.seatColumn == "B":
                return _search_next_to_in_airplane("A", seat.seatRow, airplane.seats)
            
            if seat.seatColumn == "D":
                return _search_next_to_in_airplane("E", seat.seatRow, airplane.seats)
            if seat.seatColumn == "E":
                available_seats = _search_next_to_in_airplane("D", seat.seatRow, airplane.seats)
                if not available_seats:
                    available_seats = _search_next_to_in_airplane("F", seat.seatRow, airplane.seats)
                return available_seats
            
            if seat.seatColumn == "H":
                return _search_next_to_in_airplane("I", seat.seatRow, airplane.seats)
            if seat.seatColumn == "I":
                return _search_next_to_in_airplane("H", seat.seatRow, airplane.seats)

def _search_next_to_in_airplane(col: str, row: int, airplane: list[SeatData]):
    for seat in airplane:
        if seat.seatColumn == col and seat.seatRow == row:
            return seat
    return None

def search_seat(id: int, airplane: list[SeatData]):
    """
    Busca un aasiento disponible en el avión
    Params:
        - id
        - airplane
    Returns:
        - SeatData
    """
    for seat in airplane:
        if seat.seatId == id:
            return seat
    return None

def is_next_to(seat1: SeatData, seat2: SeatData, airplane: list[SeatData], airplane_type: int):
    """
    Verifica que dos asientos sean consecutivos
    Params:
        - seat1
        - seat2
        - airplane
        -airplane_type [1, 2]
    Returns:
        - True - False
    """
    if seat1.seatRow != seat2.seatRow:
        return False
    if seat1 == seat2:
        return False
    if seat1.seatTypeId != seat2.seatTypeId:
        return False
    
    if airplane_type == 1:
        if seat1.seatTypeId == 1:
            if (seat1.seatColumn == "A" or seat2.seatColumn == "A") and (seat1.seatColumn == "B" or seat2.seatColumn == "B"):
                return True
            if (seat1.seatColumn == "F" or seat2.seatColumn == "F") and (seat1.seatColumn == "G" or seat2.seatColumn == "G"):
                return True
        else:
            if (seat1.seatColumn == "A" or seat2.seatColumn == "A") and (seat1.seatColumn == "B" or seat2.seatColumn == "B"):
                return True
            if (seat1.seatColumn == "B" or seat2.seatColumn == "B") and (seat1.seatColumn == "C" or seat2.seatColumn == "C"):
                return True
            
            if (seat1.seatColumn == "E" or seat2.seatColumn == "E") and (seat1.seatColumn == "F" or seat2.seatColumn == "F"):
                return True
            if (seat1.seatColumn == "F" or seat2.seatColumn == "F") and (seat1.seatColumn == "G" or seat2.seatColumn == "G"):
                return True
    if airplane_type == 2:
        if seat1.seatTypeId == 1:
            return False
        else:
            if (seat1.seatColumn == "A" or seat2.seatColumn == "A") and (seat1.seatColumn == "B" or seat2.seatColumn == "B"):
                return True
            
            if (seat1.seatColumn == "D" or seat2.seatColumn == "D") and (seat1.seatColumn == "E" or seat2.seatColumn == "E"):
                return True
            if (seat1.seatColumn == "E" or seat2.seatColumn == "E") and (seat1.seatColumn == "F" or seat2.seatColumn == "F"):
                return True
            
            if (seat1.seatColumn == "H" or seat2.seatColumn == "H") and (seat1.seatColumn == "I" or seat2.seatColumn == "I"):
                return True

    return False