#!/usr/bin/env python

from paho.mqtt import client as mqtt_client
import json
import random
import math

broker = 'localhost'
port = 1883
topic = "grow_room/data"

# Generate a Client ID with the subscribe prefix.
client_id = f'subscribe-{random.randint(0, 100)}'

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc, params):
        if rc == 0:
            print("Connected to MQTT Broker!")
            print("Connected with:", flags, rc, params)
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(client_id=client_id, callback_api_version=mqtt_client.CallbackAPIVersion.VERSION2)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client


def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        values = json.loads(msg.payload.decode())
        temp = float(values['temp'])
        humidity = float(values['humidity'])
        print("Temp:",temp)
        print("Humidity:",humidity)
        
        if temp > 80:
            print("Temp is too high!  Turn on the AC!")
        if humidity > 60:
            print("Humidity is too high!  Turn on the dehumidifier!")
            
        # calculate vpd, converting temp to celsius first 
        temp_celsius = (temp - 32) * 5/9
        SVP = 0.6108 * math.exp(17.27 * temp_celsius / (temp_celsius   + 237.3))
        VPD = SVP * (1 - humidity / 100)
        print("VPD:", VPD)
        
        if VPD > 1.5: 
            print("VPD is too high!  Do Somthing!!")
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()
