import json
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
        connection = await connect(self.config.RABBIT_URL)

        async with connection:
            channel = await connection.channel()

            # Объявление очереди (если не существует)
            queue_name = self.config.QUEUE_NAME
            await channel.declare_queue(queue_name)

            # Отправка сообщения
            message = self._prepare_data(data)

            # Отправка сообщения в очередь
            await channel.default_exchange.publish(message, routing_key=queue_name)

            print(f" [x] Sent kinopoisk data!")
