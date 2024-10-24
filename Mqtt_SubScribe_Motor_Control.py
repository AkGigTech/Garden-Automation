import paho.mqtt.client as mqtt
import RPi.GPIO as GPIO
import time
import threading

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
# Motor control is through GPIO 12 pin, so setting this pin as output
GPIO.setup(12, GPIO.OUT)

# Define the callback function for when a command to turn motor ON/OFF is received
def on_message(client, userdata, message):
    # Printing data on console
    print(f"Received Data is: {message.payload.decode()} on topic {message.topic}")
    if message.topic == "akrpi/motorcontrol":
        if message.payload.decode() == "1":
            # Command received to turn ON the motor
            GPIO.output(12, GPIO.HIGH)
        else:
            # Command received to turn OFF the motor
            GPIO.output(12, GPIO.LOW)

# Define the callback function for when the client connects to the broker
def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected successfully")
        # Subscribe to the topic
        client.subscribe("akrpi/motorcontrol")
    else:
        print(f"Connect failed with code {rc}")

# Function to publish heartbeat values
def publish_heartbeat(client):
    counter = 0
    while True:
        counter = 1 - counter #Toggle between 0 and 1
        print(f"Publishing heartbeat value: {counter}")
        client.publish("akrpi/heartbeatvalue", counter)
        time.sleep(3)  # Publish every 5 seconds

# Create an MQTT client instance
client = mqtt.Client()

# Set the callback functions
client.on_connect = on_connect
client.on_message = on_message

# Connect to the MQTT broker
client.connect("broker.hivemq.com", 1883, 60)

# Start a new thread to publish heartbeat values
heartbeat_thread = threading.Thread(target=publish_heartbeat, args=(client,))
heartbeat_thread.daemon = True
heartbeat_thread.start()

# Blocking call that processes network traffic, dispatches callbacks and handles reconnecting.
client.loop_forever()
