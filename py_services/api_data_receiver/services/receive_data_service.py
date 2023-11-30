import json
from datetime import datetime

from aio_pika import connect, ExchangeType, DeliveryMode, Message

from settings.config import Config


class ReceiveDataService:
    def __init__(self):
        self.config = Config()

    @staticmethod
    def _prepare_data(data: list | dict) -> Message:
        message_body = bytes(json.dumps(data), 'utf-8')

        return Message(
            message_body,
            delivery_mode=DeliveryMode.PERSISTENT,
        )

    async def send_to_rabbitmq(self, data):
        print(f'[{datetime.now()}] RECEIVER SERVICE: get data from extractor (FROM HTTP)')
        connection = await connect(self.config.RABBIT_URL)

        async with connection:
            channel = await connection.channel()

            # Объявление очереди (если не существует)
            await channel.declare_queue(self.config.QUEUE_NAME)

            # Отправка сообщения
            message = self._prepare_data(data)

            # Отправка сообщения в очередь
            await channel.default_exchange.publish(message, routing_key=self.config.QUEUE_NAME)

            print(f"[{datetime.now()}] RECEIVER SERVICE: Sent Movies data to filtration queue (TO RMQ)!")
