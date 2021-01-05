"""
In this file the valve will be controlled

Created by:
Sil van Appeldoorn
Yosri Tielbeke

https://github.com/silvappeldoorn/OSEM
"""

#22, 18 if one is high the valve is open,
#both high, both low nothing changes.
#5 always on
#19 always high first, little delay 250ms

from machine import Pin
import time
pin22 = Pin(22,Pin.OUT)
pin18 = Pin(18, Pin.OUT)
hbride_enable = Pin(5,Pin.OUT)
dcdc_enable = Pin(19,Pin.OUT)

def open():
    dcdc_enable.value(1)
    time.sleep_ms(250)
    hbride_enable.value(1)

    #swich polaritiy
    pin22.value(0)
    pin18.value(1)

def close():
    dcdc_enable.value(1)
    time.sleep_ms(250)
    hbride_enable.value(1)

    #switch polarity
    pin18.value(0)
    pin22.value(1)
   
