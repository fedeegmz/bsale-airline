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

def search_seat_by_col_and_row(col: str, row: int, airplane: list[SeatData]):
    """
    Busca un asiento por columna y fila, si no hay retorna None  
    - Param:          
        - col: str  
        - row: int  
        - airplane:  list[SeatData]  
    - Return:  
        - SeatData
    """
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
                airplane
            )
            if next_seat:
                if next_to and is_next_to(seat, next_seat):
                    return (seat.seatId, next_seat.seatId)
    
    if next_to:
        return None
    return (seat.seatId, next_seat.seatId)

def is_next_to(seat1: SeatData, seat2: SeatData):
    """
    Verifica que dos asientos sean consecutivos  
    - Param:  
        - seat1: SeatData  
        - seat2: SeatData     
    - Return:  
        - True or False
    """
    if seat1.seatRow != seat2.seatRow:
        return False
    if seat1 == seat2:
        return False
    if seat1.seatTypeId != seat2.seatTypeId:
        return False
    if abs(ord(seat1.seatColumn) - ord(seat2.seatColumn)) == 1:
        return True

def get_next_to(seat: SeatData, airplane: list[SeatData]):
    """
    Busca un asiento consecutivo y disponible (busca solo a la derecha)  
    - Param:  
        - seat: SeatData  
        - airplane: list[SeatData]  
    - Return:  
        - list[SeatData]
    """
    list_to_return = []

    next_right_seat = search_seat_by_col_and_row(
        chr(ord(seat.seatColumn) + 1),
        seat.seatRow,
        airplane
    )
    if next_right_seat:
        list_to_return.append(next_right_seat)
    
    next_left_seat = search_seat_by_col_and_row(
        chr(ord(seat.seatColumn) - 1),
        seat.seatRow,
        airplane
    )
    if next_left_seat:
        list_to_return.append(next_left_seat)
    
    if not len(list_to_return) == 0:
        return list_to_return
    return None

def get_near_seat(seat: SeatData, airplane: list[SeatData]):
    """
    Busca un asiento cerca. Primero busca en la misma fila; si no hay, busca en la misma columna.
    Si no hay retorna None  
    - Param:  
        - seat: SeatData  
        - airplane: list[SeatData]  
    - Return:  
        - SeatData
    """
    near_seat: SeatData
    next_seat = get_next_to(seat, airplane)
    if next_seat:
        return next_seat[0]
    
    near_seat = search_seat_by_col_and_row(seat.seatColumn, seat.seatRow - 1, airplane)
    
    if not near_seat or seat.seatTypeId != near_seat.seatTypeId:
        near_seat = search_seat_by_col_and_row(seat.seatColumn, seat.seatRow + 1, airplane)
    
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

def assign_seat_for_passenger(
    passenger: AccountData,
    passengers_list: list[AccountData],
    airplane: list[SeatData] = None,
    seat_id: int = None
):
    """
    Agrega un pasajero a la lista de pasajeros con asiento asignado.  
    Si se recibe el parametro seat_id se le asigna al seatId del pasajero.
    Si se recibe el parametro airplane se actualizan los lugares vacios del avion.  
    - Param:
        - passenger: AccountData  
        - passengers_list: list[AccountData]  
        - airplane: list[SeatData] = por defecto es None  
        - seat_id: int = por defecto es None
    """
    if seat_id:
        passenger.seatId = seat_id
    passengers_list.append(passenger)
    if airplane:
        update_airplane(passenger.seatId, airplane)

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
                seat.seatRow + 1,
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
                    back_seat.seatRow + 1,
                    airplane
                )
        
        if len(ids) != 0:
            data.append(ids)

    return data

def order_ready_accounts(accounts: list[AccountData]):
    """
    Ordena los pasajeros por asiento.  
    - Param:  
        - accounts: list[AccountData]  
    - Return:  
        - list[AccountData]
    """
    if len(accounts) > 1:
        half = len(accounts) // 2
        left = accounts[:half]
        right = accounts[half:]

        order_ready_accounts(left)
        order_ready_accounts(right)

        i = 0
        j = 0
        k = 0

        while i < len(left) and j < len(right):
            if left[i].seatId < right[j].seatId:
                accounts[k] = left[i]
                i += 1
            else:
                accounts[k] = right[j]
                j += 1
            
            k += 1
        
        while i < len(left):
            accounts[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            accounts[k] = right[j]
            j += 1
            k += 1
    
    return accounts


# def get_next_available_seat(seat_type: int, airplane: list[SeatData]):
#     """
#     **Generator**.  
#     Retorna el proximo lugar disponible en el avion.  
#     - Param:  
#         - seat_type: int  
#         - airplane: list[SeatData]  
#     - Yield:  
#         - SeatData
#     """
#     for seat in airplane:
#         if seat.seatTypeId == seat_type:
#             yield seat