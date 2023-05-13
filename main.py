import time
from periphery import GPIO
from multiprocessing import Process


class Unit():
    def __init__(self, pin):
        self.pin = pin
        self.pin_state = False

    def activate(self, delay):
        self.pin_state = True
        time.sleep(delay)
        print(self.pin)
        self.pin_state = False

    def getPin(self):
        return self.pin


class Task():
    def __init__(self, ammount):
        self.ammount = ammount
        self.units = []
        for i in range(ammount):
            self.units.append(Unit(10 + i))
            

    def run(self):
        print("Ammount of tasks:", self.ammount)
        for i in range(self.ammount):
            self.units[i].activate(2)


def CheckPhotoCell(old_state, new_state):
    if old_state and old_state != new_state:
        return (True, new_state)
    else:
        return (False, new_state)


if __name__ == "__main__":
    old_state = False
    #sensor = GPIO(156, "in")
    press_cnt = 3

    while True:
        bag_passed, old_state = CheckPhotoCell(old_state, (True if input("Inpu: ") == 'a' else False))
        if bag_passed:
            tmp = Task(press_cnt)
            p = Process(target=tmp.run)
            p.start()