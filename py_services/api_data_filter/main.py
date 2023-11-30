import asyncio
from services import RabbitMQService, HandlerDataService

if __name__ == "__main__":
    loop = asyncio.get_event_loop()

    async def main(loop):
        print('Start main loop!')
        handler_data = HandlerDataService()

        receive_data = RabbitMQService(handler=handler_data)
        await receive_data.get_from_rabbitmq()
        print(f'Listen: {receive_data.config.QUEUE_NAME}')


    loop.run_until_complete(main(loop))
    loop.run_forever()
