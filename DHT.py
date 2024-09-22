import Adafruit_DHT
import time

# Set the sensor type and the GPIO pin
sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO pin where the DHT11 data pin is connected

while True:
    # Read the humidity and temperature from the sensor
    humidity, temperature = Adafruit_DHT.read(sensor, pin)
    
    if humidity is not None and temperature is not None:
        print(f'Temperature: {temperature:.1f}°C  Humidity: {humidity:.1f}%')
    else:
        print('Failed to get reading. Try again!')

    # Delay for 2 seconds before the next reading
    time.sleep(2)