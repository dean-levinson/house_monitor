import asyncio
from concurrent.futures import ThreadPoolExecutor
import json
import traceback

from mongo_client import MongoClient
import aio_pika

MAX_WORKERS = 10

async def future_wrapper(future):
    await future
    try:
        future.result()
    except Exception:
        traceback.print_exc()


async def main():
    connection = await aio_pika.connect_robust(
        "amqp://guest:guest@127.0.0.1/", loop=asyncio.get_running_loop()
)

    queue_name = "computersQueue"

    db_client = MongoClient("houseMonitor", "computers")
    async with connection:
        # Creating channel
        channel = await connection.channel()

        # Declaring queue
        queue = await channel.declare_queue(queue_name)

        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as pool:
            async with queue.iterator() as queue_iter:
                async for message in queue_iter:
                    async with message.process():
                        computer = json.loads(message.body.decode())

                        asyncio.create_task(future_wrapper(
                            asyncio.get_running_loop().run_in_executor(
                                    pool, MongoClient.add_computer, db_client, computer
                                    )
                            ))


if __name__ == "__main__":
    asyncio.run(main())