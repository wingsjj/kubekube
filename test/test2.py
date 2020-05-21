import logging, kube_server, time

logging.basicConfig(level=logging.INFO)
c = kube_server.KubeServer()

while True:
  c.apply_model('test1', './abc.txt')
  time.sleep(2)

c.mqtt_client.loop_forever()