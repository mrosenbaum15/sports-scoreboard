try:
  import usocket as socket
except:
  import socket

from machine import Pin
from neopixel import NeoPixel
from time import sleep

import esp
import gc
import network

esp.osdebug(None)

gc.collect()

led = Pin(2, Pin.OUT)

print("Running")

ssid = 'Rosey iPhone'
password = '00000000'

print(ssid)
print(password)
print("Here")

station = network.WLAN(network.STA_IF)

station.active(True)

nets = station.scan()
print(nets)

station.connect(ssid, password)

while station.isconnected() == False:
  pass
 
print('Connection successful')
print(station.ifconfig())

while True:
    led.value(not led.value())
    sleep(0.5)







