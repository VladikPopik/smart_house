import RPi.GPIO as GPIO
from test_dht11 import DHT11
import time
# initialize GPIO
GPIO.setwarnings(False)
GPIO.setmode(GPIO.BOARD)
GPIO.cleanup()

# read data using pin 14
instance = DHT11(pin = 7)
result = instance.read()

while True:
    if result.is_valid():
        print("Temperature: %-3.1f C" % result.temperature)
        print("Humidity: %-3.1f %%" % result.humidity)
    else:
        print("Error: %d" % result.error_code)

    time.sleep(5)