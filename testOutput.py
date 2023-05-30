import gpio as GPIO
import multiprocessing
import time

############################## 
# Sjekk referanse for pinNum #
###########'##################
#GPIO.setup(pinNum, "out")
#GPIO.setup(pinNum, "out")
sensor = GPIO.setup(156, GPIO.IN)
presse1 = GPIO.setup(71, GPIO.OUT)
presse2 = GPIO.setup(74, GPIO.OUT)
presse3 = GPIO.setup(72, GPIO.OUT)
sensorValue = False

while True:
    print(presse1)
    GPIO.write(71, GPIO.LOW)
    time.sleep(1)
    GPIO.write(71, GPIO.HIGH)
    time.sleep(1)
    print(GPIO.read(156))
"""
pins = [71, 74, 72]
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
"""