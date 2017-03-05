import machine
import onewire
import time
import ds18x20
import network

from machine import Pin
from time import sleep_ms
from umqtt.simple import MQTTClient

class sleeper:
    def __init__(self,bb_mqtt_id="None",mqtt_broker="None",mqtt_port=0,mqtt_user="None",mqtt_passwd="None",step="None"):
        self.MINUTES_TO_SLEEP = 1
        self.SLEEP_TIME       = self.MINUTES_TO_SLEEP * 10 * 1000
        self.DONT_SLEEP       = 0
        self.MATURATION       = 1
        self.BREWING          = 0
        self.STEP             = step
        self.mqtt_broker      = mqtt_broker
        self.mqtt_port        = mqtt_port
        self.mqtt_user        = mqtt_user
        self.mqtt_passwd      = mqtt_passwd
        self.mqtt_id          = bb_mqtt_id
        self.sta_if           = network.WLAN(network.STA_IF)
        
        #fermentacao
        self.brew_low         = 17
        self.brew_ok          = 20
        self.brew_bit_high    = 22
        self.brew_very_high   = 23

        #maturacao
        self.mat_low          = 4
        self.mat_ok           = 6
        self.mat_bit_high     = 8
        self.mat_very_high    = 9
        
        #temps: low, ok, bit high, high
        self.tempFor          = {self.BREWING:[17,20,22,23], self.MATURATION:[0,4,7,9]}
        
    """Rotina a ser chamada no boot.py.
    0 - coleta temperatura e publica
    1 - fica em loop até que seja publicado que pode dormir
    2 - faz a rotina de dormir. Dorme no intervalo definido em self.SLEEP_TIME
    3 - quando der o timeout, acorda, coleta, envia e repete.
    """
    
    def now(self):
        size = 0
        while size < 11:
          try:
            size = len(self.sta_if.ifconfig()[0])
            time.sleep_ms(80)
          except:
            size = 0
            
        #coleta e publica temperatura...
        print("Coletando temperatura e publicando...")
        t = self.tasks()

        #...aguarda por ordem de dormir...
        print("Aguardando ordem para dormir...")
        self.checkIfIcanSleep()
        print("Dormindo. Ate logo.")

        #...inicia processo de deepsleep.
        rtc = machine.RTC()
        rtc.irq(trigger=rtc.ALARM0, wake=machine.DEEPSLEEP)

        #wake up
        rtc.alarm(rtc.ALARM0, self.SLEEP_TIME)

        #sleep
        machine.deepsleep()

    #chama metodo de verificacao de temperatura e publica
    def tasks(self):
        print("Lendo temperatura...")
        temperature = self.status()
        print(temperature)
        
        if not temperature is None:
            self.publish(temperature)
            return
            
        print("Nao pude fazer a leitura da temperatura")

    #pega a temperatura do DS18B20 e chama o metodo publish() para publicar no broker
    def status(self):
        ow   = onewire.OneWire(Pin(2))
        ds   = ds18x20.DS18X20(ow)
        roms = ds.scan()

        if not len(roms):
            print("Nao encontrei um dispositivo onewire.")
            return None

        ds.convert_temp()
        time.sleep_ms(750)

        temp = 0
        for i in range(10):
            for rom in roms:
                temp += ds.read_temp(rom)
        return temp/10

    #envia a temperatura para o broker
    def publish(self,valueTo):
        myMQTT = MQTTClient(self.mqtt_id,self.mqtt_broker,self.mqtt_port,self.mqtt_user,self.mqtt_passwd)
        try:
            myMQTT.connect()
            myMQTT.publish(b"beer/temperature",str(valueTo))
        except:
            print("Nao foi possivel conectar ao broker")    

    #aguarda ate que a resposta no topico seja "1" para a variavel self.DONT_SLEEP
    def checkIfIcanSleep(self):
        #fazer o subscribe
        sleep_ms(60000)
        return

    def ledControl(self,temperature):
        if self.STEP == self.BREWING:
            #blabla....
            return
