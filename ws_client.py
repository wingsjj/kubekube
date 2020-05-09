import asyncio
import websockets
import json
import logging
from json import JSONDecodeError
from websockets import WebSocketClientProtocol
from typing import Callable
import queue
from threading import Thread
import threading
import time
import concurrent

logging.basicConfig(level=logging.INFO)

class WSClient:
  def __init__(self, addr):
    super().__init__()
    self.msg_queue = queue.Queue()
    self.handlers: dict = {
      'print': print,
      'echo': self.echo,
    }
    self.addr = addr
    tt = Thread(target=w.start)
    tt.start()

  def add_handler(self, k, v:Callable[[WebSocketClientProtocol, list], None]):
    self.handlers[k] = v

  async def echo(self, websocket: WebSocketClientProtocol, args):
    await websocket.send(args)

  def send_cmd(self, cmd, args:list):
    msg = json.dumps(
        {
            'id': '%d'.format(time.time()),
            'cmd': cmd,
            'args': args
        }
    )
    send(msg)

  def send(self, msg):
    logging.info(f'sending {msg}')
    self.msg_queue.put(msg)

  async def _send_msg(self, websocket):
      while True:
        with concurrent.futures.ThreadPoolExecutor() as pool:
          msg = await asyncio.get_event_loop().run_in_executor(pool,self.msg_queue.get)
          await websocket.send(msg)

  async def _handle_msg(self, websocket):
      while True:
          msg = await websocket.recv()
          try:
            obj = json.loads(msg)
          except JSONDecodeError as e:
            logging.warning("An JSON exception occurred", e)
            logging.warning(f"invalid msg {msg}")
          if 'cmd' in obj.keys():
            func_name = obj['cmd']
            if func_name in self.handlers.keys():
              logging.info(f'handled msg {obj}')
              await self.handlers[func_name](websocket, obj['args'])
            else:
              logging.warning(f'recieved msg but no handler {msg}')

  async def _main_logic(self):
      async with websockets.connect(self.addr) as websocket:
        await asyncio.gather(self._send_msg(websocket), self._handle_msg(websocket))

  def start(self):
    loop = asyncio.new_event_loop()
    loop.run_until_complete(self._main_logic())


if __name__ == "__main__":
    w = WSClient("ws://localhost:9876/ws")
    tt = Thread(target=w.start)
    tt.start()
    time.sleep(1)
    print("abcs")
    w.send("hello")
