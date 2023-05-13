import time
from periphery import GPIO
import periphery
from multiprocessing import Process
import os

class Unit():
    def __init__(self, pin):
        self.pin = GPIO(pin, "out")

    def __del__(self):
        self.pin.close()

    def activate(self, delay):
        try:
            print(self.pin)
            self.pin.write(True)
            time.sleep(delay)
            self.pin.write(False)
        
        except periphery.GPIOError as x:
            print(x)
        

    def getPin(self):
        return self.pin.line


class Task():
    def __init__(self, ammount, pins):
        self.ammount = ammount
        self.units = []
        self.pin_array = pins
        for i in range(ammount):
            self.units.append(Unit(self.pin_array[i]))
            

    def run(self):
        for i in range(self.ammount):
            #print("PID: ", os.getpid(), " | PIN:", self.units[i].getPin())
            self.units[i].activate(0.32)


def CheckPhotoCell(old_state, new_state):
    if old_state and old_state != new_state:
        return (True, new_state)
    else:
        return (False, new_state)


def test(arr):
    for i in range(len(arr)):
        tmp = GPIO(arr[i], "out")
        tmp.write(True)
        time.sleep(1)
        tmp.write(False)
        tmp.close ()

if __name__ == "__main__":
    old_state = False
    sensor = GPIO(156, "in")
    press_cnt = 3
    pin_arr = [71, 74, 72]
    
    #test(pin_arr)

    while True:
        bag_passed, old_state = CheckPhotoCell(old_state, sensor.read())
        if bag_passed:
            tmp = Task(press_cnt, pin_arr)
            p = Process(target=tmp.run).start()