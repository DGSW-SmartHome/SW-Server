import time
import paho.mqtt.client as mqtt
import json

class MQTT:
  def __init__(self):
    self.broker = '13.209.41.37'  # mqtt broker ip
    self.port = 1883
    self.topic = '/SMARTHOME/sensor' # 하드웨어 쪽과 상의 후 변경
    self.client = None

    # sensor Value
    self.light1 = None
    self.light2 = None
    self.light3 = None


  def connect_mqtt(self) -> mqtt:
    def on_connect(client, userdata, flags, rc):
      if rc == 0:
        print('Connected to MQTT broker!')
      else:
        print('Failed to connect, return code%d\n', rc)
    
    client = mqtt.Client()
    client.on_connect = on_connect
    try:
      client.connect(self.broker, self.port)
    except ValueError:
      print("!!Cannot Connect to HOST!!")
    return client
  
  def subscribe(self, client: mqtt):
    def on_message(client, userdata, msg):
      recv = msg.payload.decode()
      HW_DATA = json.loads(recv)
      if HW_DATA:
        self.light1 = HW_DATA["light1"]
        self.light2 = HW_DATA["light2"]
        self.light3 = HW_DATA["light3"]
      else:
        print('no data...')
    
    client.subscribe(self.topic)
    client.on_message = on_message
  
  def run(self):
    self.client = self.connect_mqtt()
    self.subscribe(self.client)
    self.client.loop_start()
    print('run!')
    time.sleep(1)
    self.get_data()
  
  def get_data(self):
    if (self.light1 == None) and (self.light2 == None) and (self.light3 == None):
      returnValue = {
        "light1": 0,
        "light2": 0,
        "light3": 0
      }
      
    else:
      returnValue = {
        "light1": self.light1,
        "light2": self.light2,
        "light3": self.light3
      }

    return returnValue