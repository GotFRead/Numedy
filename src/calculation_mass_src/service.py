

import prepare

from helpers.base_service import BaseService
from helpers.broker_sender import Client
from helpers.broker_sender import TypeMessage
from helpers.database_helper import get_product_via_id
from helpers.database_helper import update_product_partial
from helpers.database_helper import get_storage_via_id
from helpers.database_helper import get_storage
from helpers.database_helper import get_all_products
from helpers.database_helper import get_all_storage
from helpers.database_helper import update_product_partial
from helpers.string_prepare import clean_string

from interfaces.warehouse.interfaces import Commands as WRCommands
from interfaces.warehouse.message_builder import ResponseBuilder as WRResponse
from interfaces.base_interface import StatusComplete

from src.models.db_helper import db_helper
from src.models.product import Product
from src.models.storage import Storage

from sqlalchemy import select

import traceback


DEFAULT_ID = -1

class Service(BaseService):
    def __init__(self) -> None:
        self.name = Client.CALC.value
        self.db_connector = db_helper
        super().__init__(self.name)

    # __product__

    async def replace_product_in_storage(self, session, product: Product):
        storage: Storage = await get_storage_via_id(
                            session=session,
                            id_=product.storage
                        )

        if storage.curr_weight + product.weight > storage.max_weight:
            raise Exception(
                'Mass over storage.max_weight < storage.curr_weight + product.weight')

        await self.patch_storage__(
            session=session,
            curr_storage=storage,
            patch_info={
                'id': storage.id,
                'address': storage.address,
                'max_weight': storage.max_weight,
                'curr_weight': storage.curr_weight + product.weight,
            }
        )


    async def replace_product_from_storage(self, session, product: Product):
        storage: Storage = await get_storage_via_id(
                            session=session,
                            id_=product.storage
                        )

        if storage.curr_weight - product.weight < 0:
            raise Exception(
                'What wrong storage.curr_weight - product.weight < 0, check your request')

        await self.patch_storage__(
            session=session,
            curr_storage=storage,
            patch_info={
                'id': storage.id,
                'address': storage.address,
                'max_weight': storage.max_weight,
                'curr_weight': storage.curr_weight - product.weight,
            }
        )
    
    async def get_next_item_id(self, list_items: list):
        if len(list_items) == 0:
            return 1
        list_ = [x.id for x in list_items]
        return max(list_) + 1

    async def add_product(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        result = dict()
        try:
            session = self.db_connector.get_scoped_session()
            
            if request['message']['product_info']['id'] == DEFAULT_ID:
                request['message']['product_info']['id'] = await self.get_next_item_id(
                    await get_all_products(self.db_connector.get_scoped_session())
                ) 

            product = Product(**request['message']['product_info'])

            await self.replace_product_in_storage(session, product)

            session.add(product)
            await session.commit()
            self.compile_product_result(result, product)

        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'add_product raise error - {msg}')
            status = StatusComplete.ERROR.value
            error = msg

            self.compile_product_result(result, request['message']['product_info'])

        return WRResponse.add_product(
            result['id'],
            result['name'],
            result['weight'],
            result['storage'],
            status,
            error,
        )

    async def remove_product(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        result = dict()
        try:
            session = self.db_connector.get_scoped_session()
            product = await get_product_via_id(
                session=session,
                product_id=request['message']['product_info']['id']
            )

            await self.replace_product_from_storage(session, product)
            await session.delete(product)
            await session.commit()

            self.compile_product_result(result, product)

            # await session.refresh() # ? Needed
        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'add_product raise error - {msg}')
            status = StatusComplete.ERROR.value
            error = msg

            self.compile_product_result(result, request['message']['product_info'])

        return WRResponse.remove_product(
            result['id'],
            result['name'],
            result['weight'],
            result['storage'],
            status,
            error,
        )
    
    def compile_product_result(self, base_obj: dict, added_obj: dict):
        for x in ['id', 'name', 'weight', 'storage']:
            if isinstance(added_obj, Product):
                base_obj[x] = getattr(added_obj, x)
            else:
                base_obj[x] = added_obj[x]

    def compile_storage_result(self, base_obj: dict, added_obj: dict):
        for x in ['id', 'address', 'max_weight', 'curr_weight']:
            if isinstance(added_obj, Storage):
                base_obj[x] = getattr(added_obj, x)
            else:
                base_obj[x] = added_obj[x]

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

            await self.replace_product_from_storage(session, product)

            product: Product = await update_product_partial(
                session=session,
                product=product,
                product_update=request['message']['product_info']
            )

            await self.replace_product_in_storage(session, product)

            await session.commit()

            self.compile_product_result(result, product)

            # await session.refresh() # ? Needed
        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'add_product raise error - {msg}')
            status = StatusComplete.ERROR.value
            self.compile_product_result(result, request['message']['product_info'])
            error = msg

        return WRResponse.patch_product(
            result['id'],
            result['name'],
            result['weight'],
            1,  # TODO Доделать запрос с storage
            status,
            error,
        )

    # __storage__

    async def add_storage(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        result = dict()
        try:
            session = self.db_connector.get_scoped_session()
            request['message']['storage_info']['curr_weight'] = 0

            if request['message']['product_info']['id'] == DEFAULT_ID:
                request['message']['product_info']['id'] = await self.get_next_item_id(
                    await get_all_storage(self.db_connector.get_scoped_session())
                ) 

            storage: Storage = Storage(**request['message']['storage_info'])
            session.add(storage)
            await session.commit()
            # await session.refresh() # ? Needed

            self.compile_storage_result(result, storage)

        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'add_storage raise error - {msg}')
            status = StatusComplete.ERROR.value
            error = msg

            self.compile_storage_result(result, request['message']['storage_info'])

        return WRResponse.add_storage(
            result['id'],
            result['address'],
            result['max_weight'],
            result['curr_weight'],
            status,
            error,
        )

    async def remove_storage(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        result = dict()
        try:
            session = self.db_connector.get_scoped_session()
            storage: Storage = await get_storage_via_id(
                session=session,
                id_=request['message']['storage_info']['id']
            )

            await session.delete(storage)
            await session.commit()

            # await session.refresh() # ? Needed

            self.compile_storage_result(result, storage)

        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'remove_storage raise error - {msg}')
            status = StatusComplete.ERROR.value
            error = msg

            self.compile_storage_result(result, request['message']['storage_info'])

        return WRResponse.remove_storage(
            result['id'],
            result['address'],
            result['max_weight'],
            result['curr_weight'],
            status,
            error,
        )
    
    async def patch_storage__(self, session, curr_storage: Storage, patch_info: dict):
        if patch_info['max_weight'] < patch_info['curr_weight']:
            raise Exception('Max weight < storage.curr_weight')

        await update_product_partial(
            session=session,
            product=curr_storage,
            product_update=patch_info
        )

        await session.commit()

    async def patch_storage(self, request: dict):
        error = ""
        status = StatusComplete.SUCCESS.value
        result = dict()
        try:
            session = self.db_connector.get_scoped_session()
            storage: Storage = await get_storage_via_id(
                session=session,
                id_=request['message']['storage_info']['id']
            )

            await self.patch_storage__(
                session,
                storage,
                request['message']['storage_info']
            )
            
            self.compile_storage_result(result, storage)

            # await session.refresh() # ? Needed
        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(f'patch_storage raise error - {msg}')
            status = StatusComplete.ERROR.value

            self.compile_storage_result(result, request['message']['storage_info'])

            error = msg

        return WRResponse.patch_storage(
            result['id'],
            result['address'],
            result['max_weight'],
            result['curr_weight'],
            status,
            error,
        )
    
    def check_intersection(self, base_string: str, checked_string: str):
        status = False
        for x in range(len(base_string)):
            if checked_string[x] == base_string[x]:
                continue
        else: 
            status = True 
        return status
    

    
    async def search_match(self, request: dict):
        error = ""

        pattern = clean_string(request['message']['product_info']['pattern']).lower()

        session = self.db_connector.get_scoped_session()

        status = StatusComplete.SUCCESS.value

        result = dict()

        try:
            result['matches'] = list()

            response = await get_all_products(session)

            for res_obj in response:
                if pattern in res_obj.name.lower():
                    result['matches'].append({
                        'id': res_obj.id,
                        'name': res_obj.name,
                        'storage': res_obj.storage,
                        'weight': res_obj.weight,
                    })

        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(msg)
            result['matches'] = list()
            error = msg
            status = StatusComplete.ERROR.value

        return WRResponse.search_product(
            result['matches'],
            status,
            error,
        )
    
    async def search_storage(self, request: dict):
        error = ""

        pattern = clean_string(request['message']['product_info']['pattern']).lower()

        session = self.db_connector.get_scoped_session()

        status = StatusComplete.SUCCESS.value

        result = dict()

        try:
            result['matches'] = list()

            response = await get_all_storage(session)

            for res_obj in response:
                if pattern in res_obj.address.lower():
                    result['matches'].append({
                        'address': res_obj.address,
                        'max_weight': res_obj.max_weight,
                        'curr_weight': res_obj.curr_weight,
                        'id': res_obj.id,
                    })

        except Exception as err:
            msg = traceback.format_exc()
            self.logger.error(msg)
            result['matches'] = list()
            error = msg
            status = StatusComplete.ERROR.value

        return WRResponse.search_storage(
            result['matches'],
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
                (TypeMessage.SET.value, WRCommands.ADD_STORAGE.value): self.add_storage,
                (TypeMessage.SET.value, WRCommands.REMOVE_STORAGE.value): self.remove_storage,
                (TypeMessage.SET.value, WRCommands.PATCH_STORAGE.value): self.patch_storage,
                (TypeMessage.GET.value, WRCommands.SEARCH_MATCH.value): self.search_match,
                (TypeMessage.GET.value, WRCommands.SEARCH_STORAGE.value): self.search_storage,
            }[type_message, command]

        except Exception as err:
            self.logger.info(
                f'Select executor raise exception - {err}, corr was stopped!')
            raise err

    def send_message(self, client_id: str, data: dict, type_message=TypeMessage.RES, receiver=Client.WEB_SERVER_WAREHOUSE_SEGMENT.value):
        self.broker_sender.send(
            initiator=client_id,
            sender=self.name,
            receiver=receiver,
            type_message=type_message.value,
            data=data,
            topic=receiver
        )
