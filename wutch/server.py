import asyncio
import pathlib
import importlib.resources as pkg_resources
import threading
from typing import Optional

import aiofiles
from aiohttp import web
from bs4 import BeautifulSoup
from loguru import logger

from .events import Event, EventDispatcher
from . import js


class Server:
    def __init__(self, config, dispatcher: Optional[EventDispatcher]) -> None:
        
        self.config = config
        self.dispatcher = dispatcher
        self.event_loop = asyncio.new_event_loop()
        self.injection_script = pkg_resources.read_text(js, "wutch.js")

        self.app = web.Application()
        self.app.add_routes([
            web.get("/ws", self.handle_websocket),
            web.get(r"/{path:.*}", self.handle_http),
        ])
        self.runner = web.AppRunner(self.app)

        self.thread = threading.Thread(
            target=self.event_loop.run_forever,
            daemon=True
        )

    async def handle_http(self, request: web.Request):
        # Returning JSON:
        # data = {"some": "data"}
        # return web.json_response(data)

        # Identify, which file was requested
        path = request.match_info["path"]
        logger.debug(f"Handling request: {path}")
        path = pathlib.Path(self.config.build_dirs[0]) / path

        if not path.exists() or not path.is_file():
            logger.error(f"File {path} not found or is not a file")
            raise web.HTTPNotFound()

        contents = None
        # Inject javascript if it's an HTML page
        if "htm" in path.suffix.lower():
            async with aiofiles.open(path, mode="r") as f:
                contents = await f.read()

            soup = BeautifulSoup(contents, "html.parser")
            if soup.head:
                script_tag = soup.new_tag("script")
                script_tag.string = self.injection_script
                soup.head.append(script_tag)
            contents = soup.prettify()

            return web.Response(
                body=contents.encode("utf-8"),
                content_type="text/html"
            )
        
        elif "css" in path.suffix.lower():
            async with aiofiles.open(path, mode="r") as f:
                contents = await f.read()
            return web.Response(text=contents, content_type="text/css")

        elif "js" in path.suffix.lower():
            async with aiofiles.open(path, mode="r") as f:
                contents = await f.read()
            return web.Response(text=contents, content_type="text/javascript")

        else:
            async with aiofiles.open(path, mode="rb") as f:
                contents = await f.read()
            return web.Response(body=contents) 

    async def handle_websocket(self, request):

        logger.debug(f"Handling websocket: {request}")
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        while True:
            await ws.send_str("reload")
            logger.debug("Hehe")
            await asyncio.sleep(1)

        return ws

    def start(self):
        
        self.thread.start()
        # Submit server running task to the event loop
        asyncio.run_coroutine_threadsafe(self._run_app(), self.event_loop)
        logger.debug("Server thread started")

    def stop(self):

        # Event loop should be properly stopped using command below.
        # But I couldn't supress the
        #   Task was destroyed but it is pending!
        # error thrown by the websocket handler when the loop got stopped.
        # So, instead, I resorted to the force thread.join with 0 timeout.
        # self.event_loop.call_soon_threadsafe(self.event_loop.stop)
        self.thread.join(timeout=0.0)
        logger.debug("Server thread stopped")

    async def _run_app(self):

        await self.runner.setup()
        site = web.TCPSite(self.runner, self.config.host, self.config.port)
        await site.start()
