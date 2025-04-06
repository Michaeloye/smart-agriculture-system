# monitor soil moisture
import RPi.GPIO as GPIO
import time
import Adafruit_DHT

channel = 21
GPIO.setmode(GPIO.BCM)
GPIO.setup(channel, GPIO.IN)

def moisture_callback(channel):
  if GPIO.input(channel):
    print("no water detected")
    # activate water pump
  else:
    print("water detected")

GPIO.add_event_detect(channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(channel, moisture_callback)

# while True:
#   time.sleep(1)

# monitor temperature
channel = 4
SENSOR = Adafruit_DHT.DHT11

def temp_callback(channel):
  humidity, temperature = Adafruit_DHT.read_retry(SENSOR, channel)

  if humidity is not None and temperature is not None:
    print(f"Temperature is {temperature:1f}C")
    print(f"Humidity is {humidity:1f}%")
  else:
    print("Failed to retrieve data from the sensor")

# while True:
#   time.sleep(1)
