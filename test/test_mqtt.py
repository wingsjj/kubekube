from client.mqtt_client import MQTTClient

c = MQTTClient("test2")
c.connect("localhost")
c.publish("hello", "test2's hello!!")