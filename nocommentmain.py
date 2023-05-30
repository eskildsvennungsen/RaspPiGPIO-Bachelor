import json
import time
import gpio as GPIO
from multiprocessing import Process
import os

class Unit():
    def __init__(self, pin):
        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def activate(self, start_delay, press_duration):
        print(start_delay, press_duration)
        time.sleep(start_delay)
        GPIO.write(self.pin, GPIO.HIGH)
        time.sleep(press_duration)
        GPIO.write(self.pin, GPIO.LOW)

    def getPin(self):
        return self.pin


class Task():
    def __init__(self, ammount, pins):
        self.ammount = ammount
        self.units = []
        self.pin_array = pins
        for i in range(ammount):
            self.units.append(Unit(self.pin_array[i]))


    def run(self, bag_size_in_m):
        first_iteration = True
        for i in range(self.ammount):
            print("PID:", os.getpid(), " | PRESS", i+1)
            self.units[i].activate(self.startDelay(bag_size_in_m, first_iteration), self.pressDuration(bag_size_in_m))
            first_iteration = False

    def startDelay(self, bag_size_in_m, is_first_iteration):
        return (((0.025 if is_first_iteration else 0.02) + (2 * bag_size_in_m)) / (3 * 0.83)) - 0.12

    def pressDuration(self, bag_size_in_m):
        return(bag_size_in_m / 0.8)

def CheckPhotoCell(old_state, new_state):
    if old_state and old_state != new_state:
        return (True, new_state)
    else:
        return (False, new_state)

def getWidthFromJSON(path):
    with open(path) as f:
        data = json.load(f)
        width = data['Settings']['width']
        f.close()
        return width

if __name__ == "__main__":
    os.system("sudo chmod a+rw /sys/class/gpio/export")
    old_state = True
    sensor = GPIO.setup(157, GPIO.IN)
    # GPIO pins: 71, 74, 73
    pin_arr = [74, 71, 73]

    while True:
        bag_passed, old_state = CheckPhotoCell(old_state, GPIO.read(157))
        if bag_passed:
            tmp = Task(len(pin_arr), pin_arr)
            bagWidth = getWidthFromJSON('/home/radxa/SRRP-GUI/build/baginfo.json') / 1000
            print(bagWidth)
            p = Process(target=tmp.run, args=(bagWidth, )).start()
