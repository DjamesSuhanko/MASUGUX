from machine import Pin
from time import sleep_ms
ledBlue = Pin(2,Pin.OUT) # ja vai acender

def myBlink(ledToBlink):
    ledToBlink.high() #apagou
    #use apenas para teste
    sleep_ms(1000)
    ledToBlink.low()
    sleep_ms(1000)

for i in range(5):
    myBlink(ledBlue)
