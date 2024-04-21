

import prepare

from helpers.base_service import BaseService
from helpers.broker_sender import Client
from helpers.broker_sender import TypeMessage
from helpers.database_helper import get_product_via_id
from helpers.database_helper import update_product_partial

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


    async def remove_product(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        try:
            session = self.db_connector.get_scoped_session()
            product = await get_product_via_id(
                session=session,
                product_id=request['message']['product_info']['id']
            )

            await session.delete(product)
            await session.commit()

            # await session.refresh() # ? Needed
        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'add_product raise error - {msg}')
            status = StatusComplete.ERROR.value
            error = msg
            
        return WRResponse.remove_product(
            product.id,
            product.name,
            product.weight,
            1, # TODO Доделать запрос с storage
            status,
            error,
        )  

    async def patch_product(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        result = dict()
        try:
            session = self.db_connector.get_scoped_session()
            product: Product = await get_product_via_id(
                session=session,
                product_id=request['message']['product_info']['id']
            )
            
            await update_product_partial(
                session=session,
                product=product,
                product_update=request['message']['product_info']
            )

            await session.commit()

            result['id'] = product.id
            result['name'] = product.name
            result['weight'] = product.weight

            # await session.refresh() # ? Needed
        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'add_product raise error - {msg}')
            status = StatusComplete.ERROR.value
            result['id'] = request['message']['product_info']['id']
            result['name'] = request['message']['product_info']['name']
            result['weight'] = request['message']['product_info']['weight']
            error = msg
            
        return WRResponse.patch_product(
            result['id'],
            result['name'],
            result['weight'],
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
                (TypeMessage.SET.value, WRCommands.REMOVE_PRODUCT.value): self.remove_product,
                (TypeMessage.SET.value, WRCommands.PATCH_PRODUCT.value): self.patch_product,
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