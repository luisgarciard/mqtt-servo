from paho.mqtt import client as mqtt_client
import random
from pyfirmata2 import Arduino, SERVO, util
from time import sleep

broker = 'broker.emqx.io'
port_mqtt = 1883
topic = "python/servo"
client_id = f'python-mqtt-{random.randint(0,1000)}'

port = "COM5"
board = Arduino(port)

servo1 = board.digital
servo1[2].mode = SERVO

def rotateservo(pin, angle):
    servo1[pin].write(angle)

def connect_mqtt():
    def on_connect(client, userdata, flags, rc, api):
        if rc == 0:
            print("Connected")
        else:
            print("Not Connected")
    client = mqtt_client.Client(client_id=client_id,callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port_mqtt)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        message = msg.payload.decode()
        
        if "move" in message:
            angle = message.split("-")[2]
            servo = int(message.split("-")[1])
            rotateservo(servo, angle)
        elif message == "reset":
            rotateservo(0)

    client.subscribe(topic)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()