


from typing import Any
from helpers.broker_sender import BrokerSender
from helpers.broker_sender import TypeMessage
from helpers.broker_sender import Client
from abc import abstractmethod

import paho.mqtt.client as mqtt
import asyncio
import json
import os


class BrokerClient:
    def __init__(self, name: str, *args, **kwargs) -> None:
        self.name = name
        self.mqtt = mqtt.Client()
        self.mqtt.on_connect = self.on_connect
        self.mqtt.on_message = self.on_message
        self.broker_sender = BrokerSender(self.mqtt, name=__name__)
        self.message_queue = asyncio.Queue()
        self.response_queue = asyncio.Queue()
        self.loop = asyncio.get_event_loop()
        self.mqtt.connect(os.getenv('MQTT_HOST', '127.0.0.1'),
                          int(os.getenv('MQTT_PORT', '1883')))
        self.mqtt.loop_start()

    def on_connect(self, client, userdata, flags, rc):
        client.subscribe([(f'>/{self.name}', 1)])

    def on_message(self, client, userdata, msg):
        asyncio.run_coroutine_threadsafe(self.message_queue.put(self.get_payload(msg)), self.loop)

    def get_payload(self, msg: object): 
        return json.loads(msg.payload.decode('utf-8'))

    @abstractmethod
    async def message_handler(self, payload: object): ...

    @abstractmethod
    async def response_handler(self, payload: object): ...