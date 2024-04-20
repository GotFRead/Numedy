

import prepare

from helpers.base_service import BaseService
from helpers.broker_sender import Client
from helpers.broker_sender import TypeMessage

from interfaces.warehouse.interfaces import Commands as WRCommands
from interfaces.warehouse.message_builder import ResponseBuilder as WRResponse
from interfaces.base_interface import StatusComplete

from src.models.db_helper import db_helper
from src.models.product import Product 

import traceback

class Service(BaseService):
    def __init__(self) -> None:
        self.name = Client.CALC.value
        self.db_connector = db_helper
        super().__init__(self.name)

    async def add_product(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        try:
            session = self.db_connector.get_scoped_session()
            product = Product(**request['message']['product_info'])
            session.add(product)
            await session.commit()
            # await session.refresh() # ? Needed
        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'add_product raise error - {msg}')
            status = StatusComplete.ERROR.value
            error = msg
            
        return WRResponse.add_product(
            product.id,
            product.name,
            product.weight,
            1, # TODO Доделать запрос с storage
            status,
            error,
        ) 

    def select_needed_handlers(self, request: dict):
        try:
            self.logger.info(f'Accept message - {request}')
            type_message = request['type_message']
            command = request['message']['command']
            
            return {
                (TypeMessage.SET.value, WRCommands.ADD_PRODUCT.value): self.add_product,
            }[type_message, command]

        except Exception as err:
            self.logger.info(f'Select executor raise exception - {err}, corr was stopped!')
            raise err
        
    def send_message(self, client_id: str, data: dict, type_message = TypeMessage.RES, receiver = Client.WEB_SERVER_WAREHOUSE_SEGMENT.value):
        self.broker_sender.send(
            initiator=client_id,
            sender=self.name,
            receiver=receiver,
            type_message=type_message.value,
            data=data, 
            topic=receiver
        )