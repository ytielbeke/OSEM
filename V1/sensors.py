"""
In this file we read all the sensors
Created by:
Sil van Appeldoorn
Yosri Tielbeke
https://github.com/silvappeldoorn/OSEM
"""

# import all the nessesery libraries
from machine import *
import dht, onewire, ds18x20, time
#import Error_Handler

# initialize all the sensors
dht_sensor = dht.DHT22(Pin(4))
dht_sensor1 = dht.DHT22(Pin(4))
onewire_temp_sensor = ds18x20.DS18X20(onewire.OneWire(Pin(14)))
hallPin = Pin(26, Pin.IN)


# the read of the DHT sensor
def read_dht (all_sensors):
    try:
        # dht = []

        dht_sensor.measure()
        room_temp = dht_sensor.temperature()
        room_hum = dht_sensor.humidity()
        print('Temperature: %3.1f C' % room_temp)
        print('Humidity: %3.1f %%' % room_hum)

        all_sensors["dht"] = [room_temp, room_hum]  # adds values from dht sensor to dictionary with 'dht' as key

    except OSError as e:
        print("Failed to read sensor.")
        # sensor_error('dht')
    return all_sensors


def read_temp_dht():
    try:
        dht_sensor1.measure()
        room_temp1 = dht_sensor1.temperature()

    except OSError as e:
        print("Failed to read sensor.")

    return room_temp1


# read the onewire temperature sensors
def read_onewire_temp (all_sensors):
    onewire_list = []
    roms = onewire_temp_sensor.scan()
    # print('Found DS devices: ', roms)
    onewire_temp_sensor.convert_temp()
    time.sleep_ms(750)
    for rom in roms:
        print(rom)
        print(20 * "-")
        print("sensor", roms.index(rom) + 1)
        print("temperature: ", onewire_temp_sensor.read_temp(rom))
        onewire_list.append(onewire_temp_sensor.read_temp(rom))

    # temperature = onewire_temp_sensor.read_temp(roms[0])
    # onewire_list.append(temperature)
    all_sensors["onewire"] = onewire_list  # adds values from onewire sensors to dictionary with 'onewire' as key
    return all_sensors


# read the waterflow sensor
def read_waterflow (all_sensors):
    pulsecount = 0
    last_value = 1
    for i in range(1):
        value = hallPin.value()
        if value == 0 and last_value == 1:
            pulsecount += 1
            last_value = value
        else:
            last_value = value

    all_sensors["waterflow"] = pulsecount  # adds value of waterflow to dictionary with 'waterflow' as key
    return all_sensors


# function makes a dictionary off all the sensors and their respective values
def read_all ():
    all_sensors = {}
    all_sensors = read_dht(all_sensors)
    all_sensors = read_onewire_temp(all_sensors)
    all_sensors = read_waterflow(all_sensors)

    return all_sensors