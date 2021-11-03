from .services.MQTT import subscribe as mqtt

mqtt = mqtt.MQTT()
mqtt.run()

def recv():
    sensorValue = mqtt.get_data()
    return sensorValue
