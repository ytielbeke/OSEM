<H1>Create a mqtt access point broker with a raspberry pi 4</H1>

al the steps are done in linux

Created by: Yosri Tielbeke


<H3>Step 1, setup raspberry pi:</H3>

on a SD card install raspberry os. 
enable ssh on the raspberry pi.
create on the boot directory a emty ssh file, open the terminal and use the following command:

```
touch ssh
```


Connect the raspberry pi to a wireless network.
***If you have a ethernet cable you can connect the raspberry pi directly to your router and go to step 2.***
Go to the rootfs of the sd card and open the 

```
sudo nano etc/wpa_supplicant/wpa_supplicant.conf
```

Put the following code in the file with your own ISO 3166-1 country code and your ssid and password of your router. 

```
ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev 
update_config=1 
country=<Insert 2 letter ISO 3166-1 country code here> 

network={ 
 ssid="<Name of your wireless LAN>" 
 psk="<Password for your wireless LAN>" 
}
```
make the ethernet port a static ip by opening the following file

```
sudo nano etc/dhcpcd.conf
```
and add the following at the bottom:
```
interface eth0 
static ip_address=192.168.137.2
```

now close the file and boot your raspberry pi.



<H3>Step 2, connect to the raspberry pi and install the software:</H3>
If you connect by an ehternet cable between your pc and the raspberry pi.
look at this link:

https://github.com/silvappeldoorn/OSEM/blob/main/ehternet.md


Find the ip of your raspberry pi.
you can use a ip scanner:

```
https://angryip.org/download/#linux
```

connect to the raspberry pi by opening a terminal and type the following:

```
ssh pi@<The ip of your raspberry pi>
```

the default password is:

```
raspberry
```

you can change this by running the command:

```
passwd
```
if in the last two lines of the code where you log in stands:
```html
Wi-Fi is currently blocked by rfkill.
Use raspi-config to set the country before use.
```

run the following command:
```
sudo rfkill unblock 0
```


Now you are connected and in your raspberry.
First update your raspberry pi

```
sudo apt-get update
```
when that is finished run 
```
sudo apt-get upgrade
```

your sudo password is also "raspberry"

install dnsmasq, hostapd and msquitto to setup your hostpot and mqtt server:

```
sudo apt-get install dnsmasq hostapd
```

<H3>Step 3, configure the hotspot:</H3>

Enable the wireless access point service
```
sudo systemctl unmask hostapd
sudo systemctl enable hostapd
```

Setup a static ip for the hotspot, open the dhcpcd.conf file
```
sudo nano /etc/dhcpcd.conf
```

And add at the bottom of the file:

```
interface wlan0
    static ip_address=192.168.4.1/24
    nohook wpa_supplicant
```

*note, if you already modified the file put this above your modified part.

Configure the dhcp and the DNS:
Save the old dns file and create a new one.
```
sudo mv /etc/dnsmasq.conf /etc/dnsmasq.conf.orig
sudo nano /etc/dnsmasq.conf
```
Add the following and save it:
```
interface=wlan0 # Listening interface
dhcp-range=192.168.4.2,192.168.4.20,255.255.255.0,24h
```

<H3>Step 4, configure the access point:</H3>
Make settings for the access point by making the file hostapd.

```
sudo nano /etc/hostapd/hostapd.conf
```

Add to the file, and edit the country_code, the ssid and the password:
```
interface=wlan0
hw_mode=g
channel=7
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_key_mgmt=WPA-PSK
wpa_pairwise=TKIP
rsn_pairwise=CCMP
country_code=<Insert 2 letter ISO 3166-1 country code here> 
ssid=<the name of the network>
wpa_passphrase=<the password of the network>
```

Now reboot your raspberry pi.
```
sudo systemctl reboot
```
***Congrats you made your hotspot***

<H3>Step 5, setup the MQTT broker</H3>

Install the nessesery programms:
```
sudo apt-get install mosquitto mosquitto-clients -y
```

Configure the settings of the MQTT broker.
Edit the mosquitto.conf file to set the settings.
```
sudo nano /etc/mosquitto/mosquitto.conf
```
***Comment the line that has conf.d included***
```
#include_dir /etc/mosquitto/conf.d
```
And set the listening port to 1883 by adding the following line at the bottom:
```
listener 1883
```

Check if the MQTT broker is running:
```
sudo systemctl status mosquitto
```

IF NOT:
```
sudo systemctl start mosquitto
```
or replace start with restart.


To always start the MQTT broker by start:
```
sudo systemctl enable mosquitto
```

You set the MQTT broker up.

<H3>TEST</H3>
To test the MQTT broker run on your raspberry pi the following command:

```
mosquitto_sub -h 192.168.4.1 -t "message"
```

On your pc first download the musquitto client:
```
sudo apt-get install mosquitto-clients -y
```
then run 
```
mosquitto_pub -h 192.168.4.1 -t "message" -m "Hello, world"
```
***You did it!!***












