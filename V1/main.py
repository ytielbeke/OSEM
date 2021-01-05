"""
This file has the main connection to the MQTT server.
The connection is setup due to Wifi.

Created by:
Sil van Appeldoorn
Yosri Tielbeke

https://github.com/silvappeldoorn/OSEM
"""


#import all the other files
import sensors
import micropython, ubinascii

#all the imports for the MQTT connection
from network import *
from umqttsimple import MQTTClient
import machine, time, esp
esp.osdebug(None)
import gc
gc.collect()

#settings for the MQTT connection
client_id = ubinascii.hexlify(machine.unique_id())
topic_sub = b'request'
topic_pub = b'sensor_value'
topic_temp = b'Rtemperature'
#topic_pub = b'hello'

roomtemperature = 20


last_message = 0
message_interval = 5
counter = 0

#settings to connect to the network
ip='192.168.4.1'
subnet = '255.255.255.0'
gateway = '192.168.4.1'
dns = '192.168.4.1'
ssid = "TinyPico"
passw = "open!source"
mqtt_server = '192.168.4.1'

#connect to the AP of the raspberry pi
def connect():
    station = WLAN(STA_IF)
    station.active(True)

    #station.ifconfig(ip, subnet, gateway, dns)
    station.connect(ssid, passw)

    print(station.ifconfig())
    print(station.isconnected())

    #print('Connection succesfull')

    return station

#connection that checks if the TinyPico is connected
def isconnected(station):
    return station.isconnected()

#checks if the raspberry pi has request information
def sub_cb(topic, msg):
    print((topic, msg))
    if topic == b'request' and msg == b'sensors':
        #result = sensors.make_dictionary()
        result = sensors.read_all()
        client.publish(topic_pub, str(result))

    if topic == b'Rtemperature':
        roomtemperature = msg

        '''       for key in result:
            print(key, result[key])
            client.publish(topic_pub, key)
            client.publish(topic_pub, str(result[key]))

        client.publish(topic_pub, result[1][0])
        client.publish(topic_pub, result[1][1])
        client.publish(topic_pub, result[1][2])
        client.publish(topic_pub, result[2][0])
    if topic == b'request' and msg == b'test':
        print("the MQTT connection is working properly")'''


#connect to the MQTT broker
def connect_and_subscribe():
    connect()
    global client_id, mqtt_server, topic_sub
    client = MQTTClient(client_id, mqtt_server)
    client.set_callback(sub_cb)
    client.connect()
    client.subscribe(topic_sub)
    client.subscribe(topic_temp)
    print('Connected to %s MQTT broker, subscribed to %s topic' % (mqtt_server, topic_sub))
    return client

#restart when the MQTT connection failed.
def restart_and_reconnect():
    print('Failed to connect to MQTT broker. Reconnecting...')
    time.sleep(10)
    machine.reset()

def fallback():
    time.sleep(1)
    if sensors.read_temp_dht()+0.2 >= roomtemperature:
        valve.close()

    if sensors.read_temp_dht()-0.2 < roomtemperature:
        valve.open()



#try to connect to the MQTT broker otherwise it resets the TinyPico
try:
    client = connect_and_subscribe()
except OSError as e:
    fallback()

#When connected to the MQTT broker it sends the info back to the Raspberrypi
while True:
  try:
    client.check_msg()
    if (time.time() - last_message) > message_interval:
      msg = b'Hello #%d' % counter
      #client.publish(topic_pub, msg)
      last_message = time.time()
      counter += 1
  except OSError as e:
    fallback()
