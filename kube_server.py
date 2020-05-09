import ftp_client
import logging
import os
import ftplib
import json
import time
from ws_client import WSClient
import mqtt_client 

class KubeServer():
    def __init__(self, host='localhost', model_path='.', ftp_port=0, mqtt_port=1883, username='kubeedge', passwd='admin'):
        self.ftp_client = ftp_client.FTPClient(host, username, passwd, ftp_port)
        self.mqtt_client = mqtt_client.MQTTClient()
        self.mqtt_client.connect(host, mqtt_port)
        self.model_path = model_path
        self.sub_topics = {
            'model_upload':'/cloud/model/upload/#',
            'param_upload':'/cloud/param/upload/#',
        }
        self.pub_topics = {
            'model_apply':'/edge/{}/model/apply',
            'param_apply':'/edge/{}/param/apply',
        }
        for topic in self.sub_topics.values():
            self.mqtt_client.subscribe(topic)
            
    def _on(self, action, callback):
      self.mqtt_client.add_handler(self.sub_topics[action], callback)

    def _pub(self, action, payload):
      self.mqtt_client.publish(self.pub_topics[action], payload)

    def on_model_upload(self, handler):
        logging.info(f'recievedon_model_upload model from topic {self.sub_topics["model_upload"]}')
        def h(msg, topic):
            node_name = topic.split('/')[-1]
            save_dir = os.path.join(self.model_path, node_name)
            self.ftp_client.download_file(msg, save_dir)
            handler(save_dir, node_name)
        self._on('model_upload', h)
        
    def on_param_upload(self, handler):
        logging.info(f'recieved model from topic {self.sub_topics["model_upload"]}')
        def h(msg, topic):
            node_name = topic.split('/')[-1]
            save_dir = os.path.join(self.model_path, node_name)
            self.ftp_client.download_file(msg, save_dir)
            handler(save_dir, node_name)
        self._on('model_upload', h)

    def apply_model(self, node_name, filename):
        if not os.path.exists(filename):
            logging.error(f"file:{filename} is not existed")
            raise FileNotFoundError
        dest = '/cloud/{}'.format(filename.split('/')[-1])
        self.ftp_client.upload_file(filename, dest)
        self._pub('model_apply', dest)

    def apply_param(self, node_name, filename):
        if not os.path.exists(filename):
            logging.error(f"file:{filename} is not existed")
            raise FileNotFoundError
        dest = f'/cloud/{filename}'
        self.ftp_client.upload_file(filename, dest)
        self._pub('param_apply', dest)

if __name__ == "__main__":
    c = KubeServer()
    c.apply_model("test1", "abc")
