import asyncio

from reach_python.consumer.queue_async_client import QueueAsyncClient
from reach_python.http_client.factory import HTTPClientFactory


class SyncReachClient:
    def __init__(self, url):
        self.url = url
        self.client = HTTPClientFactory().build("sync")

    def send_message(self, message):
        response = self.client.post(self.url + "/messages", message)
        return response


class AsyncReachClient:
    def __init__(self, url):
        self.url = url
        self.client = HTTPClientFactory().build("async")

    async def post(self, url, data=None):
        async with self.client.post(url, json=data) as resp:
            resp.raise_for_status()
            return await resp.read()

    async def send_messages(self, messages):
        responses = []
        async with self.client as session:
            tasks = []
            for message in messages:
                tasks.append(asyncio.ensure_future(self.client.post(self.url + "/messages", message)))
            tasks_gathered = await asyncio.gather(*tasks)
            for resp in tasks_gathered:
                responses.append(resp)
        return responses

    async def send_message(self, message):
        async with self.client as http:
            await http.post(self.url + "/messages", json=message)

    async def execute_action_callback(self, message, slug):
        try:
            async with self.client as http:
                response = await http.get(self.url + f"/callbacks/message/{message['id']}/slug/{slug}")
                response = await response.json()
                print(f"Response: {response}")
            return response
        except Exception as e:
            print(f"Error: {e}")


class ReachConsumerClient:
    def __init__(self, url, exchange_name):
        self.client = QueueAsyncClient(url, exchange_name)

    async def consume(self, callback, routing_key):
        await self.client.consume(callback, routing_key)
