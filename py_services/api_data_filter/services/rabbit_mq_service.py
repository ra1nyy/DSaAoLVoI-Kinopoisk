import json
from datetime import datetime

from aio_pika import connect_robust, IncomingMessage, Message, DeliveryMode, connect

from services.handler_data_service import HandlerDataService
from settings.config import Config


class RabbitMQService:
    def __init__(self, handler: HandlerDataService):
        self.config = Config()
        self._data = None
        self.handler = handler

    async def _on_message(self, message: IncomingMessage):
        print(f"[{datetime.now()}] FILTER SERVICE: Get raw Movies data to filtration ! (FROM RQM)")

        async with message.process():
            body = message.body.decode()
            self._data = json.loads(body)
            self.handler.handle_data(self._data)
            data = self.handler.get_filtered_movies()
            await self.send_to_rabbitmq(data)

    async def get_from_rabbitmq(self):
        # Подключение к RabbitMQ
        connection = await connect_robust(self.config.RABBIT_URL)
        channel = await connection.channel()

        # Объявление очереди
        queue = await channel.declare_queue(self.config.QUEUE_NAME)
        # Установка callback-функции для обработки сообщений
        await queue.consume(lambda message: self._on_message(message))

    @staticmethod
    def _prepare_data(data: list | dict) -> Message:
        message_body = bytes(json.dumps(data), 'utf-8')

        return Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

    async def send_to_rabbitmq(self, data):
        connection = await connect(self.config.RABBIT_URL)

        async with connection:
            channel = await connection.channel()

            # Отправка сообщения
            message = self._prepare_data(data)

            # Отправка сообщения в очередь
            exchange = await channel.get_exchange("log_exchange")
            await exchange.publish(message, routing_key="app_version_queue")

            print(f"[{datetime.now()}] FILTER SERVICE: Sent prepared Movies to finish queue (TO RMQ)")
