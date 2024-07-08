# data_structures
from data_structures.node import TwoWayNode

# models
from models.passenger_data import PassengerData


class Queue():

    def __init__(self) -> None:
        self.head: TwoWayNode = None
        self.tail: TwoWayNode = None
        self.__size__: int = 0
    

    def enqueue(
        self,
        data: PassengerData
    ) -> None:
        """
        Add a node to the queue
        - Param:
            - node: node to add
        """

        node = TwoWayNode(data)

        if self.head == None:
            self.head = node
            self.head.set_previous(None)
        elif self.tail == None:
            self.tail = node
            self.tail.set_previous(self.head)
            self.tail.set_next(None)
            self.head.set_next(node)
        else:
            temporal = self.tail
            temporal.set_next(node)
            node.set_next(None)
            node.set_previous(temporal)
            self.tail = node
        
        self.__size__ += 1
    

    def dequeue(self) -> PassengerData:
        """
        Remove the first node from the queue
        - Return:
            - node.get_data():  the data of the first node
        """
        if self.size() == 0:
            return None
        elif self.size() == 1:
            temporal = self.head
            self.clear()
            return temporal.get_data()
        elif self.size() == 2:
            temporal = self.head
            self.head = self.tail
            self.head.set_next(None)
            self.tail = None
            self.__size__ -= 1
            return temporal.get_data()
        
        next_node = self.head.get_next()
        temporal = self.head
        self.head = next_node
        self.__size__ -= 1
        
        return temporal.get_data()
    

    def enqueue_list(
        self,
        data: list[PassengerData]
    ) -> None:
        for item in data:
            self.enqueue(item)
        assert len(data) == self.size()


    def size(self) -> int:
        return self.__size__
    

    def iter(self) -> PassengerData:
        """
        Returns the data of the nodes one by one, from the first to the last
        """

        current = self.head
        while current:
            value = current.get_data()
            current = current.get_next()
            yield value
    

    def __iter_node__(self) -> TwoWayNode:
        """
        Returns the nodes one by one, from the first to the last
        """

        current = self.head
        while current:
            value = current
            current = current.get_next()
            yield value

    
    def remove(
        self,
        data: PassengerData
    ) -> None:
        """
        Remove a node from the queue
        - Param:
            - data: node data to delete
        """

        if data == self.head.get_data():
            self.dequeue()
        
        elif data == self.tail.get_data():
            self.tail = self.tail.get_previous()
            self.tail.set_next(None)
        
        else:
            for node in self.__iter_node__():
                if node.get_data() == data:
                    node.get_previous().set_next(node.get_next())
                    node.get_next().set_previous(node.get_previous())
    

    def clear(self):
        """
        Empty the queue
        """

        self.head = None
        self.tail = None
        self.__size__ = 0
    

    def to_list(self) -> list:
        """
        Returns a list with the data of the nodes in the queue
        """

        new_list = []
        for data in self.iter():
            new_list.append(data)
        
        return new_list


    def print(self):
        """
        Print the data of the all nodes
        """
        for data in self.iter():
            print(data)
