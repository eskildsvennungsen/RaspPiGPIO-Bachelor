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

    p1.start()
    p2.start()
    p3.start()

    p1.join()
    p2.join()
    p3.join()

"""
Tror det er lurt å lage array med pinNum og delay, og så lage en for for-løkke som lager en prosess for hver av de.
Samme med start og join.
Laget litt i farta uten mulighet for testing.
"""