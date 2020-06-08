import time
import sys
import ibmiotf.application
import ibmiotf.device
import random as r
#Provide your IBM Watson Device Credentials
organization = "u55e4o"
deviceType = "raspberrypi"
deviceId = "1103"
authMethod = "token"
authToken = "8309992798"
# Initialize GPIO
def myCommandCallback(cmd):
        print("Command received: %s" % cmd.data)
        
try:
        deviceOptions = {"org": organization, "type": deviceType, "id": deviceId, "auth-method": authMethod, "auth-token": authToken}
        deviceCli = ibmiotf.device.Client(deviceOptions)
        #.............................................
	
except Exception as e:
	print("Caught exception connecting device: %s" % str(e))
	sys.exit()
#Connect and send a datapoint "hello" with value "world" into the cloud as an event of type "greeting" 10 times
deviceCli.connect()
while True:
    hum= r.randint(0,100)
    #print(hum)
    temp = r.randint(-40,125)
    moist = r.randint(0,100)
    #Send Temperature & Humidity to IBM Watso
    data = { 'Temperature' : temp, 'Humidity': hum, 'Moisture': moist }
    #print (data)
    def myOnPublishCallback():
        print ("Published Temperature = %s C" % temp, "Humidity = %s %%" % hum, "Moisture = %s %%" % moist, "to IBM Watson")
    success = deviceCli.publishEvent("DHT11", "json", data, qos=0, on_publish=myOnPublishCallback)
    if not success:
        print("Not connected to IoTF")
    time.sleep(2)
    deviceCli.commandCallback = myCommandCallback

# Disconnect the device and application from the cloud
deviceCli.disconnect()
