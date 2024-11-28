#!/usr/bin/env python

import paho.mqtt.client as mqtt
import time
import csv
import json 
import random

rooms = ["red", "blue", "green"]
beds = ["one", "two", "three"]
if __name__ == '__main__':
  client = mqtt.Client()
  client.connect("monster.local", 1883, 60)
  
  with open('./Data/grow_room_data.csv') as csv_file:
    csv_reader = csv.DictReader(csv_file)
    for row in csv_reader:
      row["room"] = random.choice(rooms)
      row["bed"] = random.choice(beds)
      row["plant_id"] = random.randint(1,10)
      data = json.dumps(row, indent=2)
      print(data)
      client.publish('grow_room/data', data,  qos=0, retain=False)
      time.sleep(1)
  
  client.loop_forever()
