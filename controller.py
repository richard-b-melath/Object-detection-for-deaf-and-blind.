import pyfirmata
import time

comport='COM3'
board = pyfirmata.Arduino(comport)

led_1 = board.get_pin("d:11:o")
vibration = board.get_pin("d:10:o")

def vib(n):
    if n==1:
        led_1.write(1)
        vibration.write(1)
        time.sleep(1)
        led_1.write(0)
        vibration.write(0)
