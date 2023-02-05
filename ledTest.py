from machine import Pin
from time import sleep
from neopixel import NeoPixel

np = NeoPixel(Pin(22),600)

while True:
    print("Clearing")
    for i in range(0, 600):
        np[i] = (0, 0, 0)


    np.write()

    print("Running")
    for i in range(0, 100):
        np[i] = (15, 0, 0)

    np.write()
    
    sleep(2)




