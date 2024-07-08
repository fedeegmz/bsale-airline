# Pydantic
from pydantic import (
    BaseModel,
    Field
)

# models
from models.seat_data import SeatData
from models.passenger_data import PassengerData


class AirplaneData(BaseModel):
    seats: list[SeatData] = Field(...)

    def search_seat_by_id(
        self,
        seat_id: int
    ) -> SeatData | None:
        """
        Busca un asiento por ID, si no existe ese ID retorna None.
        - Param:
            - seat_id [int]
        - Return:
            - SeatData or None
        """
        for seat in self.seats:
            if seat.seat_id == seat_id:
                return seat
        return None
    
    def search_seat_by_col_and_row(
        self,
        col: str,
        row: int
    ) -> SeatData | None:
        """
        Busca un asiento por su numero de fila y su columna, si no existe retorna None.
        - Params:
            - col [str]
            - row [int]
        - Return:
            - SeatData or None
        """
        for seat in self.seats:
            if (
                seat.seat_column == col
                and seat.seat_row == row
            ):
                return seat
        return None

    def search_to_right_or_left(
        self,
        seat: SeatData,
        k: int
    ):
        """
        Search available next seats.
        - Params:
            - seat: [SeatData] -> seat of reference
            - k : {1, -1} -> 1 to search to right, -1 to search to left
        - Return: list of available seat's ids
        """
        assert k == 1 or k == -1
        
        data = []
        next_to = self.search_seat_by_col_and_row(
            chr(ord(seat.seat_column) + k),
            seat.seat_row
        )
        while next_to and not next_to.passenger_id:
            data.append(next_to.seat_id)
            next_to = self.search_seat_by_col_and_row(
                chr(ord(next_to.seat_column) + k),
                seat.seat_row
            )
        
        return data

    def search_group_of_available_seats(
        self,
        seat_type: int,
        quantity: int = 1
    ) -> SeatData | None:
        """
        Retorna un asiento que tenga cerca asientos disponibles segun la cantidad especificada.
        - Params:
            - seat_type [int]
            - quantity [int]
        - Return:
            - list[int]
        """
        assert quantity >= 1

        data = []
        for seat in self.seats:
            if seat.seat_type_id != seat_type or seat.passenger_id:
                continue
            
            data.append(seat.seat_id)
            data += self.search_to_right_or_left(seat, -1)
            data += self.search_to_right_or_left(seat, 1)

            if len(data) > 1:
                back_seat = self.search_seat_by_col_and_row(
                    seat.seat_column,
                    seat.seat_row + 1
                )
                while (
                    back_seat
                    and back_seat.seat_type_id == seat_type
                    and not back_seat.passenger_id
                ):
                    data.append(back_seat.seat_id)
                    left_seats = self.search_to_right_or_left(
                        back_seat,
                        -1
                    )
                    right_seats = self.search_to_right_or_left(
                        back_seat,
                        1
                    )
                    if len(left_seats) + len(right_seats) == 0:
                        break
                    data += left_seats
                    data += right_seats
                    
                    back_seat = self.search_seat_by_col_and_row(
                        back_seat.seat_column,
                        back_seat.seat_row + 1
                    )
            
            if len(data) >= quantity:
                # print(f"Found group of {len(data)} available seats")
                return seat
            data = []
        return None

    def is_next_to(
        self,
        seat_id_1: int,
        seat_id_2: int
    ) -> bool:
        """
        Retorna True si ambos asientos se encuentran al lado, 
        es decir si tienen la misma fila y su columna es la siguiente o la anterior.
        - Params:
            - seat_id_1 [int]
            - seat_id_2 [int]
        - Return:
            - True or False
        """
        seat_1 = self.search_seat_by_id(seat_id_1)
        seat_2 = self.search_seat_by_id(seat_id_2)

        if not seat_1 or not seat_2:
            return False
        
        if (
            (abs(ord(seat_1.seat_column) - ord(seat_2.seat_column)) == 1)
            and seat_1.seat_row == seat_2.seat_row
        ):
            return True
        return False
    
    def get_left_right_seats(
        self,
        seat_id: int,
        empty_seat: bool = True
    ) -> tuple:
        """
        Retorna (si existen y no estan ocupados) los asientos 
        de la izquierda (en la posicion 0) y de la derecha (en la posicion 1).
        - Params:
            - seat_id [int]
        - Return:
            - tuple[SeatData or None]
        """
        seat = self.search_seat_by_id(seat_id)

        next_left_seat = self.search_seat_by_col_and_row(
            chr(ord(seat.seat_column) - 1),
            seat.seat_row
        )
        if (
            empty_seat
            and next_left_seat
            and next_left_seat.passenger_id
        ):
            next_left_seat = None

        next_right_seat = self.search_seat_by_col_and_row(
            chr(ord(seat.seat_column) + 1),
            seat.seat_row
        )
        if (
            empty_seat
            and next_right_seat
            and next_right_seat.passenger_id
        ):
            next_right_seat = None
        
        return (next_left_seat, next_right_seat)

    def get_near_seat(
        self,
        seat_id: int
    ) -> SeatData | None:
        """
        Retorna un asiento que se encuentre cerca y no tenga pasajero, 
        empezando por los asientos de la misma columna, 
        siguiendo hacia adelante y luego hacia atras.
        - Params:
            - seat_id [int]
        - Return:
            - SeatData or None
        """
        next_seat = self.get_left_right_seats(seat_id)
        if next_seat[0]:
            return next_seat[0]
        if next_seat[1]:
            return next_seat[1]
        
        seat = self.search_seat_by_id(seat_id)
        assert seat
        
        near_seat = self.search_seat_by_col_and_row(
            seat.seat_column,
            seat.seat_row - 1
        )
        if (
            near_seat
            and not near_seat.passenger_id
            and seat.seat_type_id == near_seat.seat_type_id
        ):
            return near_seat
        
        near_seat = self.search_seat_by_col_and_row(
            seat.seat_column,
            seat.seat_row + 1
        )
        if (
            near_seat
            and not near_seat.passenger_id
            and seat.seat_type_id == near_seat.seat_type_id
        ):
            return near_seat
        
        return None

    def update_passenger_id(
        self,
        seat_id: int,
        passenger_id: int
    ) -> None:
        """
        Actualiza el passenger_id del asiento.
        - Params:
            - seat_id [int]
            - passenger_id [int]
        """
        seat = self.search_seat_by_id(seat_id)
        seat.passenger_id = passenger_id
    
    def update_seats(
        self,
        passengers: list[PassengerData]
    ) -> bool:
        """
        Actualiza los passenger_id de todos los asientos. 
        Retorna True si se actualizo la lista correctamente.
        - Params:
            - passengers [list[PassengerData]]
        - Return:
            - True or False
        """
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
