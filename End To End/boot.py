# This file is executed on every boot (including wake-boot from deepsleep)
try:
    import usocket as socket
except:
  import socket

import machine
import network

import neopixel
import esp
#esp.osdebug(None)

np = neopixel.NeoPixel(machine.Pin(14), 1)

np[0] = (50,0,0)
np.write()

#ssid = 'iPhone'
#password = 'thisIsWifi'
ssid = 'Rosey iPhone'
password = '00000000'

station = network.WLAN(network.STA_IF)

station.active(True)
station.connect(ssid, password)

while station.isconnected() == False:
    pass

print('Connection successful')
print(station.ifconfig())

np[0] = (0,50,0)
np.write()
