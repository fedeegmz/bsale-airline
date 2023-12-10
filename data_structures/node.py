# models
from models.passenger_data import PassengerData


class Node():

    def __init__(
        self,
        data: PassengerData,
        next = None
    ) -> None:
        self.__data__: PassengerData = data
        self.__next__ = next


    def set_next(self, node) -> bool:
        try:
            self.__next__ = node
        except:
            return False
        else:
            return True


    def get_next(self):
        return self.__next__


    def set_data(self, new_data) -> bool:
        try:
            self.__data__ = new_data
        except:
            return False
        else:
            return True


    def get_data(self) -> PassengerData:
        return self.__data__


class TwoWayNode(Node):

    def __init__(
        self,
        data,
        previous = None,
        next = None
    ) -> None:
        super().__init__(data, next)
        self.__previous__ = previous
    

    def set_previous(self, node):
        try:
            self.__previous__ = node
        except:
            return False
        else:
            return True


    def get_previous(self):
        return self.__previous__