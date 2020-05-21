import logging
import os
from client import mqtt_client, ftp_client
import tasks.task_create


class KubeServer:
    def __init__(self, host='localhost', model_path='.', ftp_port=22, mqtt_port=1883, username='kubeedge',
                 passwd='admin'):
        self.ftp_client = ftp_client.FTPClient(host, username, passwd, ftp_port)
        self.mqtt_client = mqtt_client.MQTTClient('kube_server')
        self.mqtt_client.connect(host, mqtt_port)
        self.model_path = model_path
        self.create = tasks.task_create.TaskCreate()
        self.ftp_path = 'C:/Users/SJJ/Downloads'
        self.sub_topics = {
            'model_upload': '/cloud/model/upload/#',
            'param_upload': '/cloud/param/upload/#',
            'model_train': '/cloud/model/train/#'
        }
        self.pub_topics = {
            'model_apply': '/edge/{}/model/apply',
            'param_apply': '/edge/{}/param/apply',
            'train_info': '/edge/{}/train/info'
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

    def on_model_train(self, handler):
        logging.info(f'recieved model from topic {self.sub_topics["model_train"]}')

        def h(msg, topic):
            file = self.ftp_path + topic.split('/')[-1]
            handler(file, )

        self._on('model_train', h)

    def train_model(self, node_name: str, user_id: int, filename: str):
        if not os.path.exists(filename):
            logging.error(f"train file:{filename} is not existed")
            self._pub('train_info', 'file not exist, please upload')
        dest = '/cloud/{}'.format(filename.split('/')[-1])
        file = self.ftp_path + dest
        print(file)
        self.create.create_task(user_id, file)

        # print(sub.get_all_output())
        # while sub.poll() is None:
        #     line = sub.stdout.readline()
        #     line = line.strip()
        #     if line:
        #         print('Subprogram output: [{}]'.format(line.decode('utf-8')))
        # if sub.returncode == 0:
        #     print('Subprogram success')
        # else:
        #     print('Subprogram failed')

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
    logging.getLogger().setLevel(logging.INFO)
    c = KubeServer()
    c.apply_model("test1", "train.py")
    c.train_model("test1", 1, "train.py")
    c.train_model("test1", 2, "train.py")
