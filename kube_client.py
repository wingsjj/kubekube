import logging
import os
import ftplib
import json
import time
from ws_client import WSClient
import shutil
import ftp_client
import mqtt_client


class KubeClient():
    def __init__(self, node_name, host='localhost', model_path=".", ftp_port=0, mqtt_port=1883):
        self.ftp_client = ftp_client.FTPClient(host)
        self.mqtt_client = mqtt_client.MQTTClient()
        self.model_path = model_path
        self.mqtt_client.connect(host, mqtt_port)
        self.node_name = node_name
        self.sub_topics = {
            'apply_model': f'/edge/{node_name}/model/apply',
            'apply_param': f'/edge/{node_name}/param/apply',
        }
        self.pub_topic = {
          'upload_model': '/cloud/model/upload',
            'upload_param': '/cloud/param/upload',
            'req_model': f'/cloud/{node_name}/model/request',
            'req_param': f'/cloud/{node_name}/model/request',
        }

        for topic in self.sub_topics.values():
            self.mqtt_client.subscribe(topic)

    def req_model(self):
      self._pub('req_model', self.node_name)

    def req_param(self):
      self._pub('req_param', self.node_name)

    def _on(self, action, callback):
      self.mqtt_client.add_handler(self.sub_topics[action], callback)

    def _pub(self, action, payload):
      self.mqtt_client.publish(self.pub_topic[action], payload)

    def on_apply_model(self, handler):
      def callback(filename):
        self.ftp_client.download_file(filename, self.model_path)
        handler(os.path.join(self.model_path, filename.split('/')[-1]))
      self._on('apply_model', callback)

    def on_apply_param(self, handler):
      def callback(filename):
        self.ftp_client.download_file(filename, self.model_path)
        handler(os.path.join(self.model_path, filename.split('/')[-1]))
      self._on('apply_param', callback)

    def _upload_file(self, type_name, filename):
      name = filename.split('/')[-1]
      dest = f'/{self.node_name}/{type_name}/{name}'
      self.ftp_client.upload_file(filename, dest)
      return dest

    def upload_model(self, filename):
      dest = self._upload_file('model', filename)
      self._pub('upload_model', dest)

    def upload_param(self, filename):
      dest = self._upload_file('param', filename)
      self._pub('upload_param', dest)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    c = KubeClient('test1')
    c.mqtt_client.loop_forever()
