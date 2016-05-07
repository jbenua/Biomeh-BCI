import asyncio
import datetime
from concurrent.futures import CancelledError
# from asyncio import StreamReader
loop = asyncio.get_event_loop()


async def display_date(period):
    counter = 0
    end_time = 10
    while True:
        print(datetime.datetime.now())
        if (counter + 1) >= end_time:
            break
        await asyncio.sleep(period)
        counter += 1

async def display_hello():
    counter = 0
    end_time = 10
    while True:
        print("HELLO")
        if (counter + 1) >= end_time:
            break
        await asyncio.sleep(2)
        counter += 1

loop = asyncio.get_event_loop()
date_period = int(input("Date period: "))

for o in [display_date, display_hello]:
    print(asyncio.iscoroutine(o))


tasks = [
    asyncio.ensure_future(display_date(date_period)),
    asyncio.ensure_future(display_hello())]
finished, pending = loop.run_until_complete(
    asyncio.wait(tasks, return_when=asyncio.FIRST_COMPLETED))
for task in pending:
    task.cancel()
try:
    a = loop.run_until_complete(asyncio.gather(*pending))
except CancelledError:  # Any other exception would be bad
    for task in pending:
        print("Cancelled {}: {}".format(task, task.cancelled()))
# Stop and clean up
loop.stop()
loop.close()
