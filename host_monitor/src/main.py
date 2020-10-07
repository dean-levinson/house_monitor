import asyncio
from concurrent.futures import ThreadPoolExecutor
import traceback
from traceback import print_exc

import pika

from src.monitor import Monitor, HostNotFound

count = 0
NETWORK = "10.0.0.0/24"
MAX_WORKERS = 30
NUM_OF_HOSTS = 256
SLEEP_INTERVAL = 60 * 5 # 5 min

async def scan_computers(queue: asyncio.Queue):
    monitor = Monitor(NETWORK)
    loop = asyncio.get_running_loop()
    while True:
        with ThreadPoolExecutor(MAX_WORKERS) as pool:
            aws = [loop.run_in_executor(pool, Monitor.scan_host, monitor, host) for host in monitor.get_hosts(NUM_OF_HOSTS)]
            for coro in asyncio.as_completed(aws):
                try:
                    computer = await coro
                except HostNotFound:
                    pass
                else:
                    queue.put_nowait(computer)
                
            print(f"Sleeping for {SLEEP_INTERVAL / 60} minutes...")

        await asyncio.sleep(SLEEP_INTERVAL)

async def update_result(queue: asyncio.Queue):
    global count 

    connection = pika.Connection(pika.ConnectionParameters(host='localhost'))

    channel = connection.channel()

    channel.queue_declare(queue='computersQueue')

    while True:
        computer = await queue.get()
        if computer:
            print(f"Got {computer}")
            count += 1

        channel.basic_publish(exchange='', routing_key='computersQueue', body=computer.serialize())
        print(f" [x] Sent '{computer}!'")
        queue.task_done()

    # add indication - maybe the scan_computers task (that sucks because coupled)
    connection.close()

async def main():
    import time
    start = time.time()
    data_queue = asyncio.Queue()
    scan_task = asyncio.create_task(scan_computers(data_queue))
    update_task = asyncio.create_task(update_result(data_queue))

    await scan_task
    await data_queue.join()
    update_task.cancel()
    
    print("Took:", time.time() - start)
    print("Got", count, "Computers")  

if __name__ == "__main__":
    asyncio.run(main())