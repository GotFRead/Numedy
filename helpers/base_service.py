
from helpers.logger import create_logger
from helpers.broker_client import BrokerClient

from abc import abstractmethod

import asyncio


class BaseService(BrokerClient):
    def __init__(self, name: str) -> None:
        self.name = name
        super().__init__(self.name)
        self.logger = create_logger(f'{name}.log')

    async def start(self):
        self.logger.info(f'{self.name} is STARTED!')
        await asyncio.gather(
            self.message_handler(),
            self.response_handler()
        )

    async def execute_command(self, request: dict):
        executor = self.select_needed_handlers(request)
        try:
            result = await executor(request)
        except Exception as err:
            self.logger.error(err)
            return False

        await self.response_queue.put({
            'request': request,
            'result': result
        })

    async def message_handler(self):
        while True:
            try:
                request = await self.message_queue.get()
                asyncio.run_coroutine_threadsafe(
                    self.execute_command(request), asyncio.get_running_loop())
                self.message_queue.task_done()
            except Exception as err:
                self.logger.error(err)

    async def response_handler(self):
        while True:
            try:
                response = await self.response_queue.get()

                self.send_message(
                    response['request']['initiator'],
                    response['result']
                )

                self.response_queue.task_done()
            except Exception as err:
                self.logger.error(err)

    @abstractmethod
    def select_needed_handler(self, request: dict): ...