import asyncio
from threading import Thread
from time import sleep

from aiohttp import web
from loguru import logger


async def handle(request: web.Request):
    logger.info(f"Handling request from {request.host}")
    return web.Response(text="Hello!")


app = web.Application()
app.add_routes([
    web.get("/", handle)
])
runner = web.AppRunner(app)


async def launch():

    await runner.setup()
    site = web.TCPSite(runner, "localhost", 5010)
    await site.start()
    logger.info("Site started")

    
def main():

    loop = asyncio.new_event_loop()
    thread = Thread(target=loop.run_forever, daemon=True)
    thread.start()
    logger.info("Thread started")

    # Submit async coroutine to event loop
    asyncio.run_coroutine_threadsafe(launch(), loop)

    try:
        while True:
            sleep(1)
    except KeyboardInterrupt:
        loop.call_soon_threadsafe(loop.stop)
        thread.join()

    logger.info("Thread stopped")


if __name__ == "__main__":
    main()
