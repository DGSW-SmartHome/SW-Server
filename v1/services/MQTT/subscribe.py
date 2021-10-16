import time
import paho.mqtt.client as mqtt
import json

class MQTT:
  def __init__(self):
    self.broker = ''  # mqtt broker ip
    self.port = 1883
    self.topic = 'smarthome/sensor'
    self.client = None
    
    # sensor Value
    """
    self.fineDust = None
    ... 등 이런식으로 여러가지 센서 값 변수 만들어 두기
    """
  
  def connect_mqtt(self) -> mqtt:
    def on_connect(client, userdata, flags, rc):
      if rc == 0:
        print('Connected to MQTT broker!')
      else:
        print('Failed to connect, return code%d\n', rc)
    
    client = mqtt.Client()
    client.on_connect = on_connect
    client.connect(self.broker, self.port)
    return client
  
  def subscribe(self, client: mqtt):
    def on_message(client, userdata, msg):
      recv = msg.payload.decode()
      j = json.loads(recv)
      if j:
        """  # 가져온 값을 __init__ 함수에서 만들어둔 변수에 저장
        self.fineDust = j['fine_dust']
        print('this is got : {}', format(j))  # 가져온 값 출력
        """
      else:
        ptint('no data...')
    
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
    """
    if self.fineDust == None:  # 함수에서 만들어둔 변수가 전부 None 이라면
      returnValue = {
        'fineDust': 0,
        ...
      }
      return returnValue
      
    else:
      returnValue = {
        'fineDust': self.fineDust,
        ...
      }
      return returnValue
    """