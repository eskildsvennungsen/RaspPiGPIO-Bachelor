from periphery import GPIO
import multiprocessing
import time

##############################
# Sjekk referanse for pinNum #
###########'##################
#GPIO.setup(pinNum, "out")
#GPIO.setup(pinNum, "out")
sensor = GPIO(156, "in")
sensorValue = False

pins = [1, 2, 3]
delays = [1, 2, 3]

def toggle_pin(pin_num, delay):
    while True:
        time.sleep(delay)
        print(f'Prosess {pin_num}')
        return

if __name__ == '__main__':
    while True:
        if sensor.read() != sensorValue:
            for i in range(len(pins)):
                prosess = multiprocessing.Process(target=toggle_pin, args=(pins[i], delays[i]))
                prosess.start()
            prosess.join()
        
    #print(len(pins))