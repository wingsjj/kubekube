import logging, kube_client

logging.basicConfig(level=logging.INFO)

c = kube_client.KubeClient("test1")
c.on_apply_model(print)
def on_apply_param(filename):
  print(filename)
  # do somethings
c.on_apply_param(on_apply_param)
c.upload_model('abc.txt')
c.upload_param('abc.txt')

c.mqtt_client.loop_forever()