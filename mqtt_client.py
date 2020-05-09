import paho.mqtt.client as mqtt
from paho.mqtt.client import MQTTMessage,MQTTv311
from queue import Queue
from threading import Thread
import logging

class MQTTClient(mqtt.Client):
  def __init__(self, client_id='', clean_session=None, userdata=None, protocol=MQTTv311, transport='tcp'):
    super().__init__(client_id=client_id, clean_session=clean_session, userdata=userdata, protocol=protocol, transport=transport)
    self.msg_queue = Queue()
    self.handler = {}
    self.on_message = self.on_msg
    def on_c():
      logging.info('connected')
    def on_s():
      logging.info('subscribed')
    self.on_connect = on_c
    self.on_subscribe = on_s

  def on_msg(self, client, userdata, msg:MQTTMessage):
    logging.debug(f'recieved msg topic:{msg.topic} payload:{msg.payload}')
    if msg.topic in self.handler.keys():
      self.handler[msg.topic](msg.payload.decode('utf-8'), msg.topic)

  def add_handler(self, topic, handler):
    self.handler[topic] = handler  

if __name__ == "__main__":
  c = MQTTClient("test1")
  c.connect("localhost")
  c.subscribe("/hello")
  c.publish("omg", b'hello')
  c.loop_forever()
  
