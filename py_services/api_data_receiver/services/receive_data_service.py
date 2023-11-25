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

    async def send_to_rabbitmq(self, data: list | dict):
        connection = await connect(self.config.RABBIT_URL)

        async with connection:
            channel = await connection.channel()

            logs_exchange = await channel.declare_exchange(
                "logs", ExchangeType.FANOUT,
            )

            await logs_exchange.publish(self._prepare_data(data), routing_key="info")

            print(f" [x] Sent kinopoisk data!")
