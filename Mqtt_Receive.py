import paho.mqtt.client as mqtt

import RPi.GPIO as GPIO
import time
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(21,GPIO.OUT)

# Define the callback function for when a message is received
def on_message(client, userdata, message):
    #print(f"Current Room Temperature is: {message.payload.decode()}%c on topic {message.topic}")
    print(f"Received Data is: {message.payload.decode()} on topic {message.topic}")
    #print(f"Current Room Temperature is: {message.payload.decode()}%c")
    #print(f"Current Humidity in The Room is: {message.payload.decode()}")
    if message.topic == "MotorControl":
        if message.payload.decode() == "1":
            GPIO.output(21,GPIO.HIGH)
        else:
            GPIO.output(21,GPIO.LOW)
                
    
# Define the callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to the topic
        client.subscribe("Humidity")
        client.subscribe("Temperature")
        client.subscribe("Motion")
        client.subscribe("MotorControl")
    else:
        print(f"Connect failed with code {rc}")

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
broker_address = "broker.hivemq.com"  # You can use any public MQTT broker or your own
client.connect(broker_address, 1883, 60)
try:
    # Start the loop to process network traffic and dispatch callbacks
    client.loop_forever()
except KeyboardInterrupt:
    print("Program terminated")
