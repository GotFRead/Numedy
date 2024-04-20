# coding: utf-8

import json
import time
from enum import Enum


class Client(str, Enum):
    CALC = "CALC"
    WEB_SERVER_WAREHOUSE_SEGMENT = "WEB_SERVER_WAREHOUSE_SEGMENT"

class TypeMessage(str, Enum):
    GET = 'get'
    SET = 'set'
    ACK = 'ack'
    STAT = 'stat'
    RES = 'res'
    NACK = 'nack'


class BrokerSender:
    def __init__(self, broker, name, **kwargs):
        self.broker = broker
        self.topic = name
        self.params = kwargs.copy()

    def send(self, initiator: str, sender: str, receiver: str, type_message: TypeMessage, data: dict, topic=None, id=None):
        is_command = type_message != TypeMessage.STAT
        params = self.params.copy()
        params.update(data)
        topic = f'{">" if is_command else "<"}/{self.topic if topic is None else topic}'
        payload = json.dumps({
            'id': time.time_ns() if id is None else id,
            'initiator': initiator,
            'sender': sender,
            'receiver': receiver,
            'type_message': type_message,
            'message': {**params}
        })
        # print(topic, payload)
        self.broker.publish(topic, payload)

