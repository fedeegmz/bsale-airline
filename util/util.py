# models
from models.passenger_data import PassengerData


def order_ready_passengers(passengers: list[PassengerData]):
    """
    Order the passengers by seat ID.  
    - Param:  
        - passengers: list[PassengerData]  
    - Return:  
        - ordered list[PassengerData]
    """
    if len(passengers) > 1:
        half = len(passengers) // 2
        left = passengers[:half]
        right = passengers[half:]

        order_ready_passengers(left)
        order_ready_passengers(right)

        i = 0
        j = 0
        k = 0

        while i < len(left) and j < len(right):
            if left[i].seat_id < right[j].seat_id:
                passengers[k] = left[i]
                i += 1
            else:
                passengers[k] = right[j]
                j += 1
            
            k += 1
        
        while i < len(left):
            passengers[k] = left[i]
            i += 1
            k += 1
        
        while j < len(right):
            passengers[k] = right[j]
            j += 1
            k += 1
    
    return passengers
