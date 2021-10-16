import paho.mqtt.client as mqtt
import json

broker = ''  # mqtt broker ip

class mqtt_publish():
  def __init__(self):
    self.mqtt = mqtt.Client('python_hub')     # mqtt Client 오브젝트 생성
    self.mqtt.connect(broker, 1883)           # mqtt broker에 연결
    self.mqtt.loop(2)                         # timeout - 2sec
    
  """                                         # 기본 폼
    def led(self):
    if status == 'true':
      response = {
        'type': 'led',
        'cmd': 'on'
      }
      self.mqtt.publish('smarthome/control', json.dumps(response).encode())  # topic & message 발행
    elif status == 'false':
      response = {
        'type': 'led',
        'cmd': 'off'
      }
      self.mqtt.publish('smarthome/control', json.dumps(response).encode())  # topic & message 발행
  """