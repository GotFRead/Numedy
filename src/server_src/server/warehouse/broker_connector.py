

from src.server_src.base_broker_connector import BusConnector
from interfaces.warehouse.interfaces import Commands
from interfaces.warehouse.message_builder import RequestBuilder
from helpers.broker_client import Client
from helpers.broker_sender import TypeMessage

import asyncio


class BrokerConnector:
    def __init__(self) -> None:
        self.name = Client.WEB_SERVER_WAREHOUSE_SEGMENT.value
        self.connector = BusConnector(self.name)

    async def get_response(self, client_token: str, command: Commands, timeout=60):
        command = command if isinstance(command, str) else command.value
        return await asyncio.wait_for(self.connector.wait_response(client_token, command), timeout)

    async def get_all_storage_location(self, client_id: str,): ...

    async def check_available_storage_location(self, client_id: str,): ...

    async def add_product(self,
                          client_id: str,
                          product_name: str,
                          weight: int,
                          id_: int):

        self.connector.send_message(
            client_id,
            Client.CALC.value,
            RequestBuilder.add_product(
                id_=id_,
                name=product_name,
                weight=weight
            ),
            type_message=TypeMessage.SET
        )

        try:
            result = await self.get_response(
                client_id,
                Commands.ADD_PRODUCT.value
            )
        except Exception as err:
            result = err

        return result

    async def delete_product(self, client_id: str,): ...

    async def patch_product(self, client_id: str,): ...
