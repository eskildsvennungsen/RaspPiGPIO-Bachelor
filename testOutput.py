import multiprocessing
import time

##############################
# Sjekk referanse for pinNum #
###########'##################
#GPIO.setup(pinNum, "out")
#GPIO.setup(pinNum, "out")
#GPIO.setup(156, "in") 

pins = [1, 2, 3]
delays = [1, 2, 3]

def toggle_pin(pin_num, delay):
    while True:
        time.sleep(delay)
        print(f'Prosess {pin_num}')

if __name__ == '__main__':
    for i in range(len(pins)):
        prosess = multiprocessing.Process(target=toggle_pin, args=(pins[i], delays[i]))
        prosess.start()
    prosess.join()
    #print(len(pins))