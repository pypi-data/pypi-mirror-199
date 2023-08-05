from lifty.elevator import Elevator

def test_elevator():
    elevator = Elevator(2850, 25)

    assert elevator.get_current_floor() == 1