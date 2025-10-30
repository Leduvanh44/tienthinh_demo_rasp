import paho.mqtt.client as mqtt
import json
class MQTTClient:
    def __init__(self, client_id, broker_address="test.mosquitto.org", port=1883):
        self.client_id = client_id
        self.broker_address = broker_address
        self.port = port
        self.client = mqtt.Client(self.client_id)
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.on_disconnect = self.on_disconnect
        
    def connect(self):
        try:
            self.client.connect(self.broker_address, self.port)
        except Exception as e:
            print(f"Error connecting to broker: {e}")
    
    def on_connect(self, client, userdata, flags, rc):
        print(f"Connected with result code: {rc}")
    
    def on_message(self, client, userdata, message):
        print(f"Received message: {message.payload.decode('utf-8')} on topic {message.topic}")
    
    def on_disconnect(self, client, userdata, rc):
        print(f"Disconnected with result code: {rc}")
    
    def subscribe(self, topic):
        self.client.subscribe(topic)
    
    def unsubscribe(self, topic):
        self.client.unsubscribe(topic)
    
    def publish(self, topic, message):
        message_json = json.dumps(message)
        self.client.publish(topic, message_json,retain=True)
        print(f"Published message to {topic}")
    
    def start_listening(self):
        self.client.loop_forever()
    
    def stop_listening(self):
        self.client.loop_stop()

def convert_data(names, counts, tempValues, velValues):
    data = []

    for name, count in zip(names, counts):
        value_list = []
        if "temp" in name:
            for i in range(count):
                value_list.append({"name": f"temp{i+1}{name[-2:]}", "tempValue": tempValues[i]})
        elif "vel" in name:
            for i in range(count):
                value_list.append({"name": f"vel{i+1}{name[-2:]}", "velValue": velValues[i]})
        
        data.append({"name": name, "value": value_list})

    return data
