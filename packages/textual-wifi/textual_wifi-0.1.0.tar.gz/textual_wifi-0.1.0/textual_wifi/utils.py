import asyncio as aio
import threading as th
from concurrent.futures import ThreadPoolExecutor

thread_pool = ThreadPoolExecutor(max_workers=4)


def run_background(f, *args, **kwargs):
    th.Thread(target=f, args=args, kwargs=kwargs).start()


# async def run_async(sync_function, *args, **kwargs):
#     loop = aio.get_running_loop()

#     return await loop.run_in_executor(thread_pool, sync_function, *args, **kwargs)


# def run_background(sync_function, *args, **kwargs):
#     aio.create_task(run_async(sync_function, *args, **kwargs))
