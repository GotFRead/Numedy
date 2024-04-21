

from enum import Enum

class BaseCommand(str, Enum): ...
    # ? Сделать сервисные команды?


class StatusComplete(str, Enum):
    SUCCESS = 'SUCCESS'
    ERROR = 'ERROR'
    NOT_FOUND = 'NOT FOUND'


def get_status(status: StatusComplete, error_message = '') -> str | dict:
    return status
    # TODO Переделать отправку статусов
    # return status if status == StatusComplete.SUCCESS else {
    #     'status': status,
    #     'error_message': error_message
    # }