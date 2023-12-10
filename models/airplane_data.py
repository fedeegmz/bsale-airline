# Typing
from typing import Optional

# Pydantic
from pydantic import BaseModel, Field

# models
from models.seat_data import SeatData
from models.passenger_data import PassengerData


class AirplaneData(BaseModel):
    seats: list[SeatData] = Field(...)
    cols: Optional[list[tuple[str]]] = Field(default=None)
    rows: Optional[list[tuple[int]]] = Field(default=None)

    def __init__(self, **kargs):
        super().__init__(**kargs)
        self.cols = self.__columns__()
        self.rows = self.__rows__()


    def search_seat_by_id(
        self,
        seat_id: int
    ) -> SeatData:
        for seat in self.seats:
            if seat.seat_id == seat_id:
                return seat
        assert False, "seat does not exist"
    
    def search_seat_by_col_and_row(
        self,
        col: str,
        row: int
    ) -> SeatData:
        for seat in self.seats:
            if seat.seat_column == col and seat.seat_row == row:
                return seat
        return None

    def search_group_of_empty_seats(
        self,
        seat_type: int
    ):
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
            next_to = self.search_seat_by_col_and_row(
                chr(ord(seat.seat_column) + 1),
                seat.seat_row
            )
            while next_to and next_to.seat_type_id == seat_type:
                ids_row.append(next_to.seat_id)
                next_to = self.search_seat_by_col_and_row(
                    chr(ord(next_to.seat_column) + 1),
                    seat.seat_row
                )
            
            return ids_row
        
        def search_to_rows(seat: SeatData):
            ids_rows = []
            available_seat_1 = self.search_seat_by_col_and_row(
                chr(ord(seat.seat_column) - 1),
                seat.seat_row
            )
            if available_seat_1:
                ids_rows.append(available_seat_1.seat_id)
            
            available_seat_2 = self.search_seat_by_col_and_row(
                chr(ord(seat.seat_column) + 1),
                seat.seat_row
            )
            if available_seat_2:
                ids_rows.append(available_seat_2.seat_id)
            
            return ids_rows

        data = []
        for seat in self.seats:
            ids = []
            if not seat.seat_type_id == seat_type:
                continue
            #-> seat.seatType == seat_type

            ids.append(seat.seat_id)
            ids += search_to_row(seat)
            if not len(ids) == 0:
                back_seat = self.search_seat_by_col_and_row(
                    seat.seat_column,
                    seat.seat_row + 1
                )
                while back_seat and back_seat.seat_type_id == seat_type:
                    ids.append(back_seat.seat_id)
                    row_ids = search_to_rows(back_seat)
                    if len(row_ids) == 0:
                        break
                    ids += row_ids
                    
                    back_seat = self.search_seat_by_col_and_row(
                        seat.seat_column,
                        back_seat.seat_row + 1
                    )
            
            if len(ids) != 0:
                data.append(ids)

        return data

    def search_group_of_available_seats(
        self,
        seat_type: int,
        quantity: int = 1,
        near_to: Optional[SeatData] = None
    ) -> Optional[SeatData]:
        pass

    def is_next_to(
        self,
        seat_id_1: int,
        seat_id_2: int
    ) -> bool:
        seat_1 = self.search_seat_by_id(seat_id_1)
        seat_2 = self.search_seat_by_id(seat_id_2)

        if seat_1 == seat_2:
            return False
        if seat_1.seat_row != seat_2.seat_row:
            return False
        if seat_1.seat_type_id != seat_2.seat_type_id:
            return False
        if abs(ord(seat_1.seat_column) - ord(seat_2.seat_column)) == 1:
            return True
    
    def get_left_right_seats(
        self,
        seat_id: int
    ) -> tuple:
        seat = self.search_seat_by_id(seat_id)

        next_left_seat = self.search_seat_by_col_and_row(
            chr(ord(seat.seat_column) - 1),
            seat.seat_row
        )
        if next_left_seat and next_left_seat.passenger_id:
            next_left_seat = None

        next_right_seat = self.search_seat_by_col_and_row(
            chr(ord(seat.seat_column) + 1),
            seat.seat_row
        )
        if next_right_seat and next_right_seat.passenger_id:
            next_right_seat = None
        
        return (next_left_seat, next_right_seat)

    def get_near_seat(
        self,
        seat_id: int
    ) -> Optional[SeatData]:
        next_seat = self.get_left_right_seats(seat_id)
        if next_seat[0]:
            return next_seat[0]
        if next_seat[1]:
            return next_seat[1]
        
        seat = self.search_seat_by_id(seat_id)
        
        near_seat = self.search_seat_by_col_and_row(seat.seat_column, seat.seat_row - 1)
        if near_seat and not near_seat.passenger_id and seat.seat_type_id == near_seat.seat_type_id:
            return near_seat
        
        near_seat = self.search_seat_by_col_and_row(seat.seat_column, seat.seat_row + 1)
        if near_seat and not near_seat.passenger_id and seat.seat_type_id == near_seat.seat_type_id:
            return near_seat
        
        return None

    def update_passenger_id(
        self,
        seat_id: int,
        passenger_id: int
    ) -> None:
        seat = self.search_seat_by_id(seat_id)
        seat.passenger_id = passenger_id
    
    def update_seats(
        self,
        passengers: list[PassengerData]
    ) -> bool:
        try:
            for passenger in passengers:
                if passenger.seat_id:
                    self.update_passenger_id(
                        seat_id = passenger.seat_id,
                        passenger_id = passenger.passenger_id
                    )
        except:
            return False
        return True
    

    def __columns__(self):
        list_to_return = []
        list_of_cols = list(set([seat.seat_column for seat in self.seats]))
        list_of_cols.sort()
        
        list_to_tuple = []
        for item in list_of_cols:
            if len(list_to_tuple) == 0 or abs(ord(item) - ord(list_to_tuple[-1])) == 1:
                list_to_tuple.append(item)
            else:
                list_to_return.append(tuple(list_to_tuple.copy()))
                list_to_tuple.clear()
                list_to_tuple.append(item)
        list_to_return.append(tuple(list_to_tuple.copy()))
        return list_to_return

    def __rows__(self):
        list_to_return = []
        list_of_rows = list(set([seat.seat_row for seat in self.seats]))
        list_of_rows.sort()

        list_to_tuple = []
        for item in list_of_rows:
            if len(list_to_tuple) == 0 or abs(item - list_to_tuple[-1]) == 1:
                list_to_tuple.append(item)
            else:
                list_to_return.append(tuple(list_to_tuple.copy()))
                list_to_tuple.clear()
                list_to_tuple.append(item)
        list_to_return.append(tuple(list_to_tuple.copy()))
        return list_to_return
