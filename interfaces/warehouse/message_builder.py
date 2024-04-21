
from .interfaces import Commands
from interfaces.base_interface import StatusComplete
from interfaces.base_interface import get_status

class RequestBuilder:
    @staticmethod
    def add_product(id_: int, name: str, weight: int):
        return {
            'command': Commands.ADD_PRODUCT.value,
            'product_info': {
                'id': id_,
                'name': name,
                'weight': weight,
            }
        }

    @staticmethod
    def patch_product(id_: int, name: str, weight: int):
        return {
            'command': Commands.PATCH_PRODUCT.value,
            'product_info': {
                'id': id_,
                'name': name,
                'weight': weight,
            }
        }

    @staticmethod
    def remove_product(id_: int):
        return {
            'command': Commands.REMOVE_PRODUCT.value,
            'product_info': {
                'id': id_,
            }
        }

    @staticmethod
    def storage_product(id_: int, name: str, weight: int):
        return {
            'command': Commands.ADD_STORAGE.value,
            'product_info': {
                'id': id_,
                'name': name,
                'weight': weight,
            }
        }

    @staticmethod
    def patch_storage(id_: int, name: str, weight: int):
        return {
            'command': Commands.PATCH_STORAGE.value,
            'product_info': {
                'id': id_,
                'name': name,
                'weight': weight,
            }
        }

    @staticmethod
    def remove_product(id_: int):
        return {
            'command': Commands.REMOVE_PRODUCT.value,
            'product_info': {
                'id': id_,
            }
        }

class ResponseBuilder:
    @staticmethod
    def add_product(id: int, name: str, weight: int, storage: int, status: StatusComplete = StatusComplete.SUCCESS, error_message: str = ''):
        return {
            'command': Commands.ADD_PRODUCT.value,
            'status': get_status(status, error_message),
            'product_info': {
                'id': id,
                'name': name,
                'weight': weight,
                'storage': storage
            }
        }
    
    @staticmethod
    def remove_product(id: int, name: str, weight: int, storage: int, status: StatusComplete = StatusComplete.SUCCESS, error_message: str = ''):
        return {
            'command': Commands.REMOVE_PRODUCT.value,
            'status': get_status(status, error_message),
            'product_info': {
                'id': id,
                'name': name,
                'weight': weight,
                'storage': storage
            }
        }
    

    @staticmethod
    def patch_product(id: int, name: str, weight: int, storage: int, status: StatusComplete = StatusComplete.SUCCESS, error_message: str = ''):
        return {
            'command': Commands.PATCH_PRODUCT.value,
            'status': get_status(status, error_message),
            'product_info': {
                'id': id,
                'name': name,
                'weight': weight,
                'storage': storage
            }
        }