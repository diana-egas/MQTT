import random
import time

from paho.mqtt import client as mqtt_client
from gpio import led



broker = 'broker.emqx.io'
port = 1883

topic1 = "python/led"
topic2 = "python/mqtt2"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 1000)}'
username = 'emqx'
password = 'public'

def value():
    led_status = led()
    print("...",led_status)
    return led_status 

def connect_mqtt():
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)

    return client

def publish(client):
    msg_count = 0

    while True:
        time.sleep(3)
        msg = str(value())
        result = client.publish(topic1, msg) # result: [0, 1]
        status = result[0]

        if status == 0:
            print(f"Send `{msg}` to topic `{topic1}`")
        else:
            print(f"Failed to send message to topic {topic1}")
        
        msg_count += 1

        time.sleep(3)
        msg = "ola2"
        result = client.publish(topic2, msg) # result: [0, 1]
        status = result[0]

        if status == 0:
            print(f"Send `{msg}` to topic `{topic2}`")
        else:
            print(f"Failed to send message to topic {topic2}")
        
        msg_count += 1

def run():
    client = connect_mqtt()
    client.loop_start()
    publish(client)

if __name__ == '__main__':
    run()
