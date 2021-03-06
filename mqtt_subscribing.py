import random

from paho.mqtt import client as mqtt_client
from sound import sound_temperature

broker = 'broker.emqx.io'
port = 1883

topic1 = "LED"
topic2 = "TEMPERATURE"

# generate client ID with pub prefix randomly
client_id = f'python-mqtt-{random.randint(0, 100)}'
username = 'hot client'
password = 'public'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.username_pw_set("emqx", "public")
    
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"{username}:Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        sound_temperature(msg.payload.decode(), msg.topic)

    client.subscribe(topic1)
    client.subscribe(topic2)
    client.on_message = on_message

def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()

if __name__ == '__main__':
    run()
