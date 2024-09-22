#mqtt code
import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
#DHI Code
import Adafruit_DHT
import time

# Set the GPIO mode
GPIO.setmode(GPIO.BCM)

#DHT code
# Set the sensor type and the GPIO pin
sensor = Adafruit_DHT.DHT11
pin = 4  # GPIO pin where the DHT11 data pin is connected
# Set the GPIO pin for the PIR sensor
pir_pin = 17

# Set up the PIR pin as an input
GPIO.setup(pir_pin, GPIO.IN)

# Define the callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
    else:
        print(f"Connect failed with code {rc}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback function
client.on_connect = on_connect

# Connect to the MQTT broker
broker_address = "broker.hivemq.com"  # You can use any public MQTT broker or your own
client.connect(broker_address, 1883, 60)

# Start the loop to process network traffic and dispatch callbacks
client.loop_start()
print("PIR Sensor Test (CTRL+C to exit)")
try:
    while True:
        # Read the humidity and temperature from the sensor
        humidity, temperature = Adafruit_DHT.read(sensor, pin)
        motion = GPIO.input(pir_pin)    
        topic = "Motion"
        client.publish(topic, motion)
        #print(f"Published message: {message} to topic: {topic}")
        print(f"Current status is {motion} on topic: {topic}")
        # Publish a message to a topic
        topic = "Humidity"
        #message = "humidity, temperature"
        #message = humidity
        #RH = (100 - humidity)
        client.publish(topic, humidity)
        print(f"Current Humidity is {humidity} on topic: {topic}")
        topic = "Temperature"
        client.publish(topic, temperature)
        #print(f"Published message: {message} to topic: {topic}")
        print(f"Current Temperature Is {temperature}%c on topic: {topic}")
        # Delay for 10 seconds before the next reading
        time.sleep(10)
except KeyboardInterrupt:
    print("Program Terminated")
# Stop the loop and disconnect from the broker
client.loop_stop()
client.disconnect()
