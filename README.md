# domoticz

Here is a collection of my domoticz scripts.

| Script name | description |
|--|--|
| check_device_online.py | check if mac address is on network |

## check_device_online
Parameters

| name | description |
|--|--|
| mac | mac address to search on network |
| idx | switch index to update |
| url | base url of domoticz server without http(s):// and any / (default : localhost) |
| user | user for basic auth if needed |
| password | password of basic auth if needed |

This script check if mac address is on network and update domoticz switch if mac is present.
If domoticz server is protected you can use basic auth with parameter

To run this script correctly you need to have `arp-scan` installed on your system and user runing script have to be in sudoers :
`sudo apt-get install arp-scan`

A good way to call this script is by crontab :
`* * * * * sudo python /home/pi/domoticz/scripts/check_device_online.py 01:23:45:67:89:ab 1`