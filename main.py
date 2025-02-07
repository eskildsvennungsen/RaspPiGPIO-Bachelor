##
# @mainpage Description
# Python program for paralell controll of SRRP-modules. When a bag
# passes the photocell, a new task is created with an array of SRRP-units.
# It's then launced in parallel.
# Copyrigth (c) 2023 HOLDT - Hull og Lekkasje Deteksjons Teknologi. All rights reserved.

##
# @file main.py
# @brief Controlles the whole sequence.
#
# @section author_doxygen Author (s)
# - Eskild Dybwad Svennungsen
# - Kristoffer Solheim


# Imports
import json
import numpy as np
import time
import gpio as GPIO
from multiprocessing import Process
import os

class Unit():
    def __init__(self, pin):
        '''! Initializes a unit(single SRRP-moduel).
        @param self The module to controll.
        @param pin The GPIO pin number to controll the unit.
        '''

        self.pin = pin
        GPIO.setup(pin, GPIO.OUT)

    def activate(self, start_delay, press_duration):
        '''!Activates the module for a given duration.
        @param self The module to controll.
        @param delay The ammount of time before the bag is in the correct position
        '''
        print(start_delay, press_duration)
        time.sleep(start_delay)
        GPIO.write(self.pin, GPIO.HIGH)
        time.sleep(press_duration)
        GPIO.write(self.pin, GPIO.LOW)

    def getPin(self):
        '''! Return the GPIO controll pin for the module.
        @return GPIO pin-number.
        '''
        return self.pin


class Task():
    def __init__(self, ammount, pins):
        '''! Initializes a task
        @brief A Task is initialized with an array of \b Unit (s).
        @param ammount The ammount of \b SRRP-modules in use.
        @param pin Array of pins that controll the modules.
        @return GPIO pin-number.
        '''
        self.ammount = ammount
        self.units = []
        self.pin_array = pins
        for i in range(ammount):
            self.units.append(Unit(self.pin_array[i]))


    def run(self, bag_size_in_m):
        '''! Runs task.
        @brief Iterates through the task sequentially.
        '''
        first_iteration = True
        for i in range(self.ammount):
            print("PID:", os.getpid(), " | PRESS", i+1)
            self.units[i].activate(self.startDelay(bag_size_in_m, first_iteration), self.pressDuration(bag_size_in_m))
            first_iteration = False

    def startDelay(self, bag_size_in_m, is_first_iteration):
        '''! Calculates delay before a press starts.
        @param bag_size_in_m Uses the bagsize as variable to calculate delay
        @param is_first_iteration Longer distance to first press, first iteration returns longer delay.
        @return Delay for press to start
        '''
        return (((0.025 if is_first_iteration else 0.02) + (2 * bag_size_in_m)) / (3 * RMPtoMS(36))) - 0.12

    def pressDuration(self, bag_size_in_m):
        '''! Calculates the duration of the press.
        @return Duration for the press.
        '''
        return(bag_size_in_m / 0.8)

def CheckPhotoCell(old_state, new_state):
    '''! Checks the photocell if a new bag has passed.
    @brief A new bag is considered to be in the system when it has fully
    passed the photocell. We check this by comparing the old_state to the
    new_state.
    @code
        if old_state and old_state != new_state
    @endcode
    @param old_state The previous state of the photocell.
    @param new_state The current state of the photocell.

    @return (True, new_state) If bag has passed.
    @return (False, new_state If bag has not passed.
    '''
    if old_state and old_state != new_state:
        return (True, new_state)
    else:
        return (False, new_state)

def getWidthFromJSON(path):
    '''! Returns width of bag that's being analyzed.
    @param path Filepath to the json file containing bag information.
    @return width Return width of given bag.
    '''
    with open(path) as f:
        data = json.load(f)
        width = data['Settings']['width']
        f.close()
        return width

def RMPtoMS(rpm):
    return(0.046 * np.pi * rpm /60)


if __name__ == "__main__":
    os.system("sudo chmod a+rw /sys/class/gpio/export")
    old_state = True
    sensor = GPIO.setup(157, GPIO.IN)
    # GPIO pins: 71, 74, 73
    pin_arr = [74, 71, 73]

    # /home/radxa/build-SRRP-GUI-Desktop-Debug/baginfo.json
    # /home/radxa/SRRP-GUI/build/baginfo.json
    while True:
        bag_passed, old_state = CheckPhotoCell(old_state, GPIO.read(157))
        if bag_passed:
            tmp = Task(len(pin_arr), pin_arr)
            bagWidth = getWidthFromJSON('/home/radxa/SRRP-GUI/build/baginfo.json') / 1000
            print(bagWidth)
            p = Process(target=tmp.run, args=(bagWidth, )).start()
