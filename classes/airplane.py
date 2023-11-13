# Python
from typing import Optional

# database
from database.mysql_client import conn

# schemas
from schemas.seat import seat


class Airplane:
    
    def __init__(
        self,
        data: Optional[list],
        id: Optional[int],
        search: bool = False
    ) -> None:
        self.data = data
        if search and isinstance(id, int):
            self.data = self.__getdata__(id)

    def __getdata__(self, id: int):
        """
        Returns a set of seats on the airplane.
        - Params:
            - id: airplane ID
        """
        query: str = f'SELECT s.seat_id, s.seat_column, s.seat_row, s.seat_type_id '\
                    f'FROM airline.seat AS s '\
                    f'WHERE s.airplane_id = {id}'
        # cursor.execute(query)
        # self.data = cursor.fetchall()

        self.data = conn.execute(seat.select().where(seat.airplane_id == id)).fetchall()
