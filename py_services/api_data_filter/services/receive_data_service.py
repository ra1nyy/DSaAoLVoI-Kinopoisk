import json

from aio_pika import connect_robust, IncomingMessage

from services.handler_data_service import HandlerDataService
from settings.config import Config


class ReceiveDataService:
    def __init__(self, handler: HandlerDataService):
        self.config = Config()
        self._data = None
        self.handler = handler

    async def _on_message(self, message: IncomingMessage):
        print(f" [x] Get kinopoisk data!")

        async with message.process():
            body = message.body.decode()
            self._data = json.loads(body)
            self.handler.handle_data(self._data)

    async def get_from_rabbitmq(self):
        # Подключение к RabbitMQ
        connection = await connect_robust(self.config.RABBIT_URL)
        channel = await connection.channel()

        # Объявление очереди
        queue = await channel.declare_queue(self.config.QUEUE_NAME)
        # Установка callback-функции для обработки сообщений
        await queue.consume(lambda message: self._on_message(message))
