import time

from umqtt.simple import MQTTClient
from machine import Pin
import network
# Publish test messages e.g. with:
# mosquitto_pub -t foo_topic -m hello

class freezer:
    def __init__(self,bb_mqtt_id="None",mqtt_broker="None",mqtt_port=0,mqtt_user="None",mqtt_passwd="None",topic="None"):
        self.relay_one = Pin(12,Pin.OUT) 
        self.relay_two = Pin(13,Pin.OUT)

        self.bb_mqtt_id   = "ElectroDragon"
        self.mqtt_broker  = mqtt_broker
        self.mqtt_port    = mqtt_port
        self.mqtt_user    = mqtt_user
        self.mqtt_passwd  = mqtt_passwd
        self.topic        = topic
        self.mqtt         = MQTTClient(self.bb_mqtt_id,self.mqtt_broker,self.mqtt_port,self.mqtt_user,self.mqtt_passwd)
        self.sta_if       = network.WLAN(network.STA_IF)

        self.programs     = {"fermentation":[18.0,22.0],"maturation":[0.0,2.0],"priming":[23.0,25.0]}

        self.MINIMUM      = self.programs["fermentation"][0]
        self.MAXIMUM      = self.programs["fermentation"][1]
        
        print("Waiting IP...")
        size = 0
        while size < 11:
          try:
            size = len(self.sta_if.ifconfig()[0])
            time.sleep_ms(80)
          except:
            size = 0

        self.mqtt.connect()

    def doSleep(self):
        try:
            #self.mqtt.connect()
            self.mqtt.publish(b"beer/sleep",b'1')
        except:
            print("Nao foi possivel conectar ao broker")

    def toNumber(self,target):
        if len(target) == 4:
            temp  = (target[0] - 48) * 10.0
            temp += (target[1] - 48) *  1.0
            temp += (target[3] - 48) *  0.1

        elif len(target) == 3:
            if not target.find(b'.') == 1:
                return 0.0

            temp  = (target[0] - 48) * 1.0
            temp += (target[2] - 48) * 0.1

        self.doSleep()
        return temp
                
    # Received messages from subscriptions will be delivered to this callback
    def sub_cb(self,topic, msg):
        print((topic, msg))

        if topic == b'beer/program':
            temp = str(msg)
            if temp in self.programs.keys():
                self.MINIMAL = programs[step][0]
                self.MAXIMUM = programs[step][1]
                
        elif topic == b'beer/temperature':
            temp = self.toNumber(msg)
            if temp > self.MAXIMUM:
                self.relay_one.high()
                print("relay ON")
            
            elif temp < self.MINIMUM:
                print("relay OFF")
                self.relay_one.low()

    def check(self,server="192.168.1.2"):
        print("Connecting...")
        print("Setting callback...")
        self.mqtt.set_callback(self.sub_cb)
        #self.mqtt.connect()
        print("Subscribe to beer/temperature...")
        self.mqtt.subscribe(b"beer/#")
        while True:
            if True:
                # Blocking wait for message
                self.mqtt.wait_msg()
            else:
                # Non-blocking wait for message
                self.mqtt.check_msg()
                # Then need to sleep to avoid 100% CPU usage (in a real
                # app other useful actions would be performed instead)
                time.sleep(1)

        self.mqtt.disconnect()
