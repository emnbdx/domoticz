import base64
from os.path import expanduser
import json
import logging
import subprocess
import sys
import urllib2

# try to get argv value, return none if not existing
def read_argument(index):
	try:
		return sys.argv[index]
	except IndexError:
		return None

# make http call, add authorization header is user and password passed to this script
def http_request(url):
	logging.debug("Call http url : %s" % url)
	request = urllib2.Request(url)
	if not url_user and not url_password:
		base_64_string = base64.encodestring("%s:%s" % (url_user, url_password)).replace("\n", "")
		request.add_header("Authorization", "Basic %s" % base_64_string)
	response = urllib2.urlopen(request)
	return response.read()

# check if mac address is on network to simplify return On if present, Off else
def check_mac():
	mac_on_network = 0 == subprocess.call("sudo arp-scan --interface=eth0 --localnet | grep " + mac + " > /dev/null", shell=True)
	
	if mac_on_network:
		return "On"
	else:
		return "Off"

# get current state on server
def check_device_state():
	response = http_request("http://%s/json.htm?type=devices&rid=%s" % (url_base, idx))
	json_object = json.loads(response)
	return json_object["result"][0]["Status"]

mac = read_argument(1)
idx = read_argument(2)
url_base = read_argument(3) or "localhost"
url_user = read_argument(4)
url_password = read_argument(5)

FORMAT = '%(asctime)-15s %(message)s'
print (expanduser("~"))
logging.basicConfig(filename="%s/log" % expanduser("~"),level=logging.DEBUG, format=FORMAT)

real = check_mac()
domoticz = check_device_state()

logging.debug("Mac %s : domoticz %s" % (real, domoticz))

if real != domoticz:
	logging.info("update state on domoticz")
	http_request("http://%s/json.htm?type=command&param=switchlight&idx=%s&switchcmd=%s" % (url_base, idx, real))
else:
	logging.info("no need to update")
