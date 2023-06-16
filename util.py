from models import AccountData, SeatData

def group_accounts(accounts: list[AccountData]):
    """
    Agrupa los pasajeros que tiene asientos y los que no  
    - Param:  
        - accounts: list[AccountData]  
    - Return:  
        - accounts_to_update: list[AccountData]  
        - accounts_ready: list[AccountData]
    """
    accounts_to_update: list[AccountData] = []
    accounts_ready: list[AccountData] = []
    children: list[AccountData] = []
    n = 0
    for account in accounts:
        if account.age < 18:
            children.append(account)
        elif account.seatId:
            accounts_ready.append(account)
        elif not account.seatId:
            accounts_to_update.append(account)
        n += 1

    return (accounts_to_update, accounts_ready, children)

def get_parents(child: AccountData, accounts1: list[AccountData], accounts2: list[AccountData]):
    """
    Busca pasajeros con igual purchaseId  
    - Param:  
        - child: AccountData  
        - accounts: list[AccountData]  
    - Return:  
        - list[AccountData]
    """
    list_to_return = []
    n = 0
    while n < len(accounts1):
        if accounts1[n].purchaseId == child.purchaseId:
            list_to_return.append(
                accounts1.pop(n)
            )
            n -= 1
        n += 1
    
    m = 0
    while m < len(accounts2):
        if accounts2[m].purchaseId == child.purchaseId:
            list_to_return.append(
                accounts2.pop(m)
            )
            m -= 1
        m += 1
    
    if len(list_to_return) == 0:
        return None
    
    return list_to_return


def search_seat_by_id(id: int, airplane: list[SeatData]):
    """
    Busca el asiento por id. Si no existe retorna None  
    - Param:  
        - id: int  
        - airplane: list[SeatData]  
    - Return:  
        - SeatData
    """
    for seat in airplane:
        if seat.seatId == id:
            return seat
    return None

def search_seat_by_col_and_row(col: str, row: str, airplane: list[SeatData]):
    """
    Busca un asiento por columna y fila, si no hay retorna None  
    - Param:          
        - col: str  
        - row: int  
        - airplane:  list[SeatData]  
    - Return:  
        - SeatData
    """
    col = str(col)
    row = str(row)

    for seat in airplane:
        if seat.seatColumn == col and seat.seatRow == row:
            return seat
    return None

def search_seat_for_two_passengers(
    seat_type: int,
    airplane: list[SeatData],
    airplane_type: int,
    next_to: bool = False
):
    """
    Busca dos asientos disponibles que sean del mismo seatTypeId  
    - Param:  
        - seat_type: int  
        - airplane: list[SeatData]  
        - next_to: bool -> si deben estar al lado si o si  
    - Return:  
        - (seatId, seatId) -> una tupla con dos id
    """
    for seat in airplane:
        if seat.seatTypeId == seat_type:
            next_seat = get_near_seat(
                seat,
                airplane,
                airplane_type
            )
            if next_seat:
                if next_to and is_next_to(seat, next_seat, airplane_type):
                    return (seat.seatId, next_seat.seatId)
    
    if next_to:
        return None
    return (seat.seatId, next_seat.seatId)

def is_next_to(seat1: SeatData, seat2: SeatData, airplane_type: int):
    """
    Verifica que dos asientos sean consecutivos  
    - Param:  
        - seat1: SeatData  
        - seat2: SeatData  
        - airplane: list[SeatData]  
        - airplane_type: int  
    - Return:  
        - True or False
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

def get_next_to(seat: SeatData, airplane: list[SeatData], airplane_type: int):
    """
    Busca un asiento consecutivo y disponible  
    - Param:  
        - seat: SeatData  
        - airplane: list[SeatData]  
        - airplane_type: int  
    - Return:  
        - SeatData
    """
    if airplane_type == 1:
        if seat.seatTypeId == 1:
            if seat.seatColumn == "A":
                return search_seat_by_col_and_row("B", seat.seatRow, airplane)
            if seat.seatColumn == "B":
                return search_seat_by_col_and_row("A", seat.seatRow, airplane)
            if seat.seatColumn == "F":
                return search_seat_by_col_and_row("G", seat.seatRow, airplane)
            if seat.seatColumn == "G":
                return search_seat_by_col_and_row("F", seat.seatRow, airplane)
        else:
            if seat.seatColumn == "A":
                return search_seat_by_col_and_row("B", seat.seatRow, airplane)
            if seat.seatColumn == "B":
                available_seats = search_seat_by_col_and_row("A", seat.seatRow, airplane)
                if not available_seats:
                    available_seats = search_seat_by_col_and_row("C", seat.seatRow, airplane)
                return available_seats
            if seat.seatColumn == "C":
                return search_seat_by_col_and_row("B", seat.seatRow, airplane)
            
            if seat.seatColumn == "E":
                return search_seat_by_col_and_row("F", seat.seatRow, airplane)
            if seat.seatColumn == "F":
                available_seats = search_seat_by_col_and_row("E", seat.seatRow, airplane)
                if not available_seats:
                    available_seats = search_seat_by_col_and_row("G", seat.seatRow, airplane)
                return available_seats
            if seat.seatColumn == "G":
                return search_seat_by_col_and_row("F", seat.seatRow, airplane)
    elif airplane_type == 2:
        if seat.seatTypeId == 1:
            return None
        else:
            if seat.seatColumn == "A":
                return search_seat_by_col_and_row("B", seat.seatRow, airplane)
            if seat.seatColumn == "B":
                return search_seat_by_col_and_row("A", seat.seatRow, airplane)
            
            if seat.seatColumn == "D":
                return search_seat_by_col_and_row("E", seat.seatRow, airplane)
            if seat.seatColumn == "E":
                available_seats = search_seat_by_col_and_row("D", seat.seatRow, airplane)
                if not available_seats:
                    available_seats = search_seat_by_col_and_row("F", seat.seatRow, airplane)
                return available_seats
            
            if seat.seatColumn == "H":
                return search_seat_by_col_and_row("I", seat.seatRow, airplane)
            if seat.seatColumn == "I":
                return search_seat_by_col_and_row("H", seat.seatRow, airplane)

def get_near_seat(seat: SeatData, airplane: list[SeatData], airplane_type: int):
    """
    Busca un asiento cerca. Primero busca en la misma fila; si no hay, busca en la misma columna.
    Si no hay retorna None  
    - Param:  
        - seat: SeatData  
        - airplane: list[SeatData]  
        - airplane_type: int  
    - Return:  
        - SeatData
    """
    near_seat: SeatData = get_next_to(seat, airplane, airplane_type)
    
    if near_seat:
        return near_seat
    
    near_seat = search_seat_by_col_and_row(seat.seatColumn, str(int(seat.seatRow) - 1), airplane)
    
    if not near_seat or seat.seatTypeId != near_seat.seatTypeId:
        near_seat = search_seat_by_col_and_row(seat.seatColumn, str(int(seat.seatRow) + 1), airplane)
    
    if near_seat:
        return near_seat
    return None

def update_airplane(seat_id: int, airplane: list[SeatData]):
    """
    Actualiza los lugares vacios en el avion. Elimina de la lista de lugares vacios el asiesto por param  
    - Param:  
        - seat_id: int  
        - airplane: list[SeatData]
    - Return:  
        - SeatData
    """
    n = 0
    for seat in airplane:
        if seat.seatId == seat_id:
            return airplane.pop(n)
        n += 1

def get_next_available_seat(seat_type: int, airplane: list[SeatData]):
    """
    **Generator**.  
    Retorna el proximo lugar disponible en el avion.  
    - Param:  
        - seat_type: int  
        - airplane: list[SeatData]  
    - Yield:  
        - SeatData
    """
    for seat in airplane:
        if seat.seatTypeId == seat_type:
            yield seat

def search_group_of_empty_seats(seat_type: int, airplane: list[SeatData]):
    """
    Busca grupos de asientos disponibles
    - Param:
        - seat_type: int
        - airplane: list[SeatData]
    - Return:
        - list[list] -> lista con listas de grupos de seatId disponibles
    """

    def search_to_row(seat: SeatData):
        ids_row = []
        next_to = search_seat_by_col_and_row(
            chr(ord(seat.seatColumn) + 1),
            seat.seatRow,
            airplane
        )
        while next_to and next_to.seatTypeId == seat_type:
            ids_row.append(next_to.seatId)
            next_to = search_seat_by_col_and_row(
                chr(ord(next_to.seatColumn) + 1),
                seat.seatRow,
                airplane
            )
        
        return ids_row
    
    def search_to_rows(seat: SeatData):
        ids_rows = []
        available_seat_1 = search_seat_by_col_and_row(
            chr(ord(seat.seatColumn) - 1),
            seat.seatRow,
            airplane
        )
        if available_seat_1:
            ids_rows.append(available_seat_1.seatId)
        
        available_seat_2 = search_seat_by_col_and_row(
            chr(ord(seat.seatColumn) + 1),
            seat.seatRow,
            airplane
        )
        if available_seat_2:
            ids_rows.append(available_seat_2.seatId)
        
        return ids_rows

    data = []
    for seat in airplane:
        ids = []
        if not seat.seatTypeId == seat_type:
            continue
        #-> seat.seatType == seat_type

        ids.append(seat.seatId)
        ids += search_to_row(seat)
        if not len(ids) == 0:
            back_seat = search_seat_by_col_and_row(
                seat.seatColumn,
                str(int(seat.seatRow) + 1),
                airplane
            )
            while back_seat and back_seat.seatTypeId == seat_type:
                ids.append(back_seat.seatId)
                row_ids = search_to_rows(back_seat)
                if len(row_ids) == 0:
                    break
                ids += row_ids
                
                back_seat = search_seat_by_col_and_row(
                    seat.seatColumn,
                    str(int(back_seat.seatRow) + 1),
                    airplane
                )
        
        if len(ids) != 0:
            data.append(ids)

    return data

def order_ready_accounts(accounts: list[AccountData]):
    pass