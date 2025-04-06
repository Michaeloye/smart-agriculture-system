import RPi.GPIO as GPIO
import Adafruit_DHT
import time

SENSOR = Adafruit_DHT.DHT11

moisture_channel = 15
pump_channel = 23
temp_channel = 4

temperature_range = (25, 33) # celsius, for germination process. Range is 25, 33(inclusive) for vegetative growth
humidity_range = (50, 60) # in percentage

GPIO.setmode(GPIO.BCM)
GPIO.setup(moisture_channel, GPIO.IN)
GPIO.setup(pump_channel, GPIO.OUT)

soil_has_moisture = False
current_temperature = 0
current_humidity = 0

def moisture_callback(channel):
    global soil_has_moisture

    if GPIO.input(channel):
        soil_has_moisture = False
        print("Dry: Activate water pump")
    else:
        soil_has_moisture = True
        print("Wet: water detected")

GPIO.add_event_detect(moisture_channel, GPIO.BOTH, bouncetime=300)
GPIO.add_event_callback(moisture_channel, moisture_callback)

def read_temperature_humidity(pin):
    global current_temperature, current_humidity

    humidity, temperature = Adafruit_DHT.read_retry(SENSOR, pin)

    if humidity is not None and temperature is not None:
        current_temperature = temperature
        current_humidity = humidity

        print(f"Temperature: {temperature:.1f}C, Humidity: {humidity:.1f}%")
    else:
        print("Failed to retrieve data from the sensor")

def handle_watering():
    if not soil_has_moisture:
        if current_temperature > temperature_range[1] and current_humidity < humidity_range[0]:
            # hot and dry air => high need for water
            GPIO.output(pump_channel, GPIO.LOW)
            print("Turning ON the pump...: low soil moisture, high temperature, low humidity")
        elif current_temperature > temperature_range[1]:
            # hot air, increased transpiration, likely need for water
            GPIO.output(pump_channel, GPIO.LOW)
            print("Turning ON the pump...: low soil moisture and high temperature")
        elif current_humidity < humidity_range[0]:
            # dry air will draw moisture from soil
            GPIO.output(pump_channel, GPIO.LOW)
            print("Turning ON the pump...: low soil moisture and low humidity")
        else:
            # soil is dry, but air conditions are not extreme
            GPIO.output(pump_channel, GPIO.LOW)
            print("Turning ON the pump...: low soil moisture")
    
# Main Loop
try:
    while True:
        read_temperature_humidity(temp_channel)
        time.sleep(2)  # Read every 2 seconds

except KeyboardInterrupt:
    print("Program terminated by user.")
    GPIO.cleanup()