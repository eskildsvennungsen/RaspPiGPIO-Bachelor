from periphery import GPIO
import multiprocessing
import time

##############################
# Sjekk referanse for pinNum #
###########'##################
#GPIO.setup(pinNum, "out")
#GPIO.setup(pinNum, "out")
GPIO.setup(156, "in") 

def toggle_pin(pin_num, delay):
    pin_state = False
    while True:
        GPIO.write(pin_num, pin_state)
        pin_state = not pin_state
        time.sleep(delay)

if __name__ == '__main__':
    p1 = multiprocessing.Process(target=toggle_pin, args=(pinNum, 1))
    p2 = multiprocessing.Process(target=toggle_pin, args=(pinNum, 2))
    p3 = multiprocessing.Process(target=toggle_pin, args=(pinNum, 3))

    
    while GPIO.read(156) == True:
        time.sleep(0.1)

    p1.start()
    time.sleep(0.5) 
    p2.start()

    p1.join()
    p2.join()
