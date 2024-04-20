from helpers.broker_client import BrokerClient
from helpers.broker_sender import Client
from helpers.broker_sender import TypeMessage
from interfaces.base_interface import BaseCommand

import asyncio

class BusConnector(BrokerClient):
    def __init__(self, name = 'DEFAULT_NAME') -> None:
        self.name = name
        super().__init__(self.name)
        self.mqtt.on_connect = self.__on_connect
        self.mqtt.on_message = self.__on_message
        self.response = dict()
        self.lock = asyncio.Lock()

    def send_message(self, 
                    initiator: str,
                    receiver: str,
                    data: dict = {},
                    type_message: TypeMessage = TypeMessage.GET,):
        
        self.broker_sender.send(
            initiator=initiator,
            sender=self.name,
            receiver=receiver,
            type_message=type_message.value,
            data=data,
            topic=receiver
        )

    async def wait_response(self, session_token: str, message_code: str):
        while True:
            params = (session_token, message_code)
            async with self.lock:
                if params not in self.response.keys() or self.response[params] is None:
                    result = None
                elif self.response[params] == []:
                    result = []
                else: 
                    result = self.response[params].copy()

            if result is None:
                await asyncio.sleep(0.1)
            else:
                del self.response[params]
                return result
            
    async def clear_response_pool_before_send_request(self, session_token: str, message_code: BaseCommand):
        async with self.lock:
            key = (session_token, message_code)
            if key in self.response: 
                del self.response[key]

    def __on_connect(self, client, userdata, flags, rc):
        client.subscribe([(f'>/{self.name}', 1)])

    def __on_message(self, client, userdata, msg):
        payload = self.get_payload(msg)
        self.response[(payload['initiator'], payload['message']['command'])] = payload['message']
