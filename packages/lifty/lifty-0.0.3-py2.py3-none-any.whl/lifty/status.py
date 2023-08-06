from enum import Enum

class Door(Enum):
    CLOSING = 1
    OPENING = 2
    CLOSED = 3
    OPENED = 4

class Elevator(Enum):
    STOPPED = 1
    MOVING_UP = 2
    MOVING_DOWN = 3
    STOPPING = 4