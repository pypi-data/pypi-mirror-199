from enum import Enum
from . import status

class Elevator:
    def __init__(self, weight_capacity: int, num_of_floors: int):
        self.__weight_capacity = weight_capacity
        self.__current_floor = 1
        self.__num_of_floors = num_of_floors
        self.__elevator_door_status = status.Door.CLOSED
        self.__elevator_status = status.Elevator.STOPPED
        self.__current_direction = status.Elevator.STOPPED
        self.__floors = []

    def __str__(self):
        return f'Elevator(Current floor: {self.__current_floor}, Elevator door status: {self.__elevator_door_status}, Elevator status: {self.__elevator_status})'

    def get_weight_capacity(self) -> int:
        return self.__weight_capacity
    
    def get_current_floor(self) -> int:
        return self.__current_floor
    
    def get_number_stops(self) -> int:
        return len(self.floors)
    
    def get_direction(self) -> status.Elevator:
        return self.__current_direction
    
    def get_door_status(self) -> status.Elevator:
        return self.__elevator_door_status
    
    def get_status(self) -> status.Elevator:
        return self.__elevator_status

    def select_floor(self, floor_number: int) -> None:
        self.__floors.append(floor_number)

    def emergency_stop(self) -> None:
        self.__elevator_status = status.Elevator.STOPPING
        self.__elevator_status = status.Elevator.STOPPED

    def close_doors(self) -> None:
        self.__elevator_door_status = status.Door.CLOSING
        self.__elevator_door_status = status.Door.CLOSED

    def open_doors(self) -> None:
        if self.__elevator_status == status.Elevator.STOPPED:                
            self.__elevator_door_status = status.Door.OPENING
            self.__elevator_door_status = status.Door.OPENED

    def call_elevator(self, floor_number: int) -> None:
        self.__floors.append(floor_number)

    def move(self) -> None:
        check_floor = 0
        if len(self.__floors) > 1:
            check_floor = len(self.__floors) - 1

        if self.__current_floor >= self.__floors[check_floor]:
            self.__current_direction = status.Elevator.MOVING_DOWN
            self.__current_floor -= 1

            for floor in self.__floors:
                if floor == self.__current_floor:
                    self.__floors.remove(floor)
                    self.open_doors()
                    self.close_doors()
        
        else:
            self.__current_direction = status.Elevator.MOVING_UP
            self.__current_floor += 1

            for floor in self.__floors:
                if floor == self.__current_floor:
                    self.__floors.remove(floor)
                    self.open_doors()
                    self.close_doors()
