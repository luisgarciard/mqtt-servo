from paho.mqtt import client as mqtt_client
import random
from pyfirmata2 import Arduino, SERVO, util
import time

broker = 'broker.emqx.io'
port_mqtt = 1883
topic = "python/servo"
client_id = f'python-mqtt-{random.randint(0,1000)}'

port = "/dev/ttyUSB0"
board = Arduino(port)

   

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
        print(message)
        
        if "start" in message:
            servo_pins = [2,3,4,5]
            angles = [90,50,60,60]
            delay_between_moves = 1
            
            for servo_pin, angle in zip(servo_pins, angles):
                board.digital[servo_pin].mode = SERVO
                board.digital[servo_pin].write(angle)
                time.sleep(delay_between_moves)

            client.publish(topic, "takeright")
            servo2_pins = [2,3,4,5]
            angles2 = [90,150, 70, 70]

            for servo_pin, angle in zip(servo2_pins, angles2):
                board.digital[servo_pin].mode = SERVO
                board.digital[servo_pin].write(angle)
                time.sleep(delay_between_moves)
            client.publish(topic, "takeleft")
            
            servo3_pins = [2,3,4,5]
            angles3 = [90,90,90,90]

            for servo_pin, angle in zip(servo3_pins, angles3):
                board.digital[servo_pin].mode = SERVO
                board.digital[servo_pin].write(angle)
                time.sleep(delay_between_moves)
            client.publish(topic, "taketop")

            servo4_pins = [2,3,4,5]
            angles4 = [0,50,60,60]

            for servo_pin, angle in zip(servo4_pins, angles4):
                board.digital[servo_pin].mode = SERVO
                board.digital[servo_pin].write(angle)
                time.sleep(delay_between_moves)
            client.publish(topic, "takeback")

            servo5_pins = [2,3,4,5]
            angles5 = [180,40,60,40]

            for servo_pin, angle in zip(servo5_pins, angles5):
                board.digital[servo_pin].mode = SERVO
                board.digital[servo_pin].write(angle)
                time.sleep(delay_between_moves)
            client.publish(topic, "takefront")
                
        elif "move" in message:
            angle = message.split("-")[2]
            servo = int(message.split("-")[1])

            board.digital[servo].mode = SERVO
            board.digital[servo].write(angle)
            
        elif "reset" in message:
            servo = int(message.split("-")[1])
            board.digital[servo].mode = SERVO
            board.digital[servo].write(0)

    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

run()
