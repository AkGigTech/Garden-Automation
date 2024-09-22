import RPi.GPIO as GPIO
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

# Set the GPIO pin for the PIR sensor
pir_pin = 26

# Set up the PIR pin as an input
GPIO.setup(pir_pin, GPIO.IN)

print("PIR Sensor Test (CTRL+C to exit)")

# Loop to continuously check for motion
try:
    while True:
        WaterLevel = GPIO.input(pir_pin)
        print(f"Current Water Level is: {WaterLevel}")
        time.sleep(1)  # Delay for 1 second
except KeyboardInterrupt:
    print("Program terminated")
finally:
    GPIO.cleanup()
