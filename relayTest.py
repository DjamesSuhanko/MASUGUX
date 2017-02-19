from machine import Pin
from time import sleep_ms

relay_one = Pin(12,Pin.OUT)
relay_two = Pin(13,Pin.OUT)

relays = [relay_one,relay_two]

for relay in relays:
    relay.high()
    sleep_ms(1000)
    relay.low()
