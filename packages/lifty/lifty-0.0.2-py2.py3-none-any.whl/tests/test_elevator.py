from lifty.elevator import Elevator

def test_elevator():
    elevator = Elevator(2850, 25)

    assert elevator.get_current_floor() == 1

    elevator.call_elevator(5)
    elevator.move()
    elevator.move()
    elevator.move()
    elevator.move()

    assert elevator.get_current_floor() == 5

    elevator.select_floor(2)
    elevator.move()
    elevator.move()
    elevator.move()

    assert elevator.get_current_floor() == 2
