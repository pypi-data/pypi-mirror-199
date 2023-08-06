import json

import aio_pika


class QueueAsyncClient:
    def __init__(self, url, exchange_name):
        self.url = url
        self.exchange_name = exchange_name
        self.connection = None
        self.channel = None
        self.exchange = None

    async def consume(self, callback, routing_key):
        connection = await self._get_connection()
        async with connection:
            if self.exchange is None:
                self.exchange = await self.channel.declare_exchange(
                    self.exchange_name,
                    aio_pika.ExchangeType.FANOUT
                )

            queue = await self.channel.declare_queue(exclusive=True)
            await queue.bind(self.exchange, routing_key=routing_key)

            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        decoded_message = message.body.decode('utf-8')
                        payload = json.loads(decoded_message)
                        await callback(payload)

    async def close(self):
        if self.connection:
            await self.connection.close()

    async def _get_connection(self):
        if self.connection is None or self.connection.is_closed:
            self.connection = await aio_pika.connect_robust(self.url)

        if self.channel is None or self.channel.is_closed:
            self.channel = await self.connection.channel()

        return self.connection

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.close()
