import paho.mqtt.client as mqtt
import json

broker = '13.209.41.37'  # mqtt broker ip
topic = '/SMARTHOME/contorl'


class mqtt_publish:
    def __init__(self):
        self.mqtt = mqtt.Client('python_hub')  # mqtt Client 오브젝트 생성
        self.mqtt.connect(broker, 1883)  # mqtt broker에 연결
        self.mqtt.loop(2)  # timeout - 2sec

    def roomPlug(self, status, plugNumber):
        command = 'on' if status else 'off'
        returnData = {
            'type': "plug"+str(plugNumber),
            'cmd': command
        }
        self.mqtt.publish(topic, json.dumps(returnData).encode())

    def roomLight(self, status, lightNumber):
        returnData = {
            'type': "light"+str(lightNumber),
            'cmd': status
        }
        self.mqtt.publish(topic, json.dumps(returnData).encode())

    """                                         # 기본 폼
    def led(self):
    if status == 'true':
      response = {
        'type': 'led',
        'cmd': 'on'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())  # topic & message 발행
    elif status == 'false':
      response = {
        'type': 'led',
        'cmd': 'off'
      }
      self.mqtt.publish(topic, json.dumps(response).encode())  # topic & message 발행
  """
