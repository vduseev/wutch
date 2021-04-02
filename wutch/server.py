import asyncio
import pathlib
import importlib.resources as pkg_resources
import threading
from typing import Optional
import webbrowser

import aiofiles
from aiohttp import web
from bs4 import BeautifulSoup
from loguru import logger

from .threaded import Threaded
from .events import Event, EventDispatcher
from . import js


class Server(Threaded):
    def __init__(self, config, dispatcher: EventDispatcher) -> None:

        self.config = config
        self.dispatcher = dispatcher
        self.injection_script = pkg_resources.read_text(js, "wutch.js")

        # Initialize async thread and web server application
        self.event_loop = asyncio.new_event_loop()
        self.app = web.Application()
        self.app.add_routes([
            web.get("/ws", self.handle_websocket),
            web.get(r"/{file:.*}", self.handle_http),
        ])
        self.runner = web.AppRunner(self.app)
        self.thread = threading.Thread(
            target=self.event_loop.run_forever,
            daemon=True
        )

    def start(self):

        self.thread.start()
        # Submit server running task to the event loop
        asyncio.run_coroutine_threadsafe(
            self._start_async_runner(), self.event_loop)
        logger.debug("Server thread started")

        if self.config.index and not self.config.no_browser:
            self._open_browser()

    def stop(self):

        # Event loop should be properly stopped using command below.
        # But I couldn't supress the
        #   "Task was destroyed but it is pending!"
        # error thrown by the websocket handler when the loop got stopped.
        # So, instead, I resorted to the force thread.join with 0 timeout.
        # self.event_loop.call_soon_threadsafe(self.event_loop.stop)
        self.thread.join(timeout=0.0)
        logger.debug("Server thread stopped")

    async def handle_http(self, request: web.Request):

        # Identify path of the requested file
        file = request.match_info["file"]
        logger.debug(f"Handling request: {file}")
        path = pathlib.Path(self.config.build) / file

        if not path.exists() or not path.is_file():
            logger.error(f"File {path} not found or is not a file")
            raise web.HTTPNotFound()

        if "htm" in path.suffix.lower():
            return await self._load(path, content_type="text/html", content_modifier=self._inject_script)

        elif "css" in path.suffix.lower():
            return await self._load(path, content_type="text/css")

        elif "js" in path.suffix.lower():
            return await self._load(path, content_type="text/javascript")

        else:
            return await self._load(path, mode="rb", content_type="application/octet-stream")

    async def handle_websocket(self, request):

        logger.debug(f"Handling websocket: {request}")
        ws = web.WebSocketResponse()
        await ws.prepare(request)

        while True:
            if self.dispatcher.count(Event.ShellCommandFinished):
                # Claim all events
                self.dispatcher.claim(Event.ShellCommandFinished)
                await ws.send_str("reload")
                logger.debug("Reload message sent via websocket")

            await asyncio.sleep(1)

        return ws

    async def _start_async_runner(self):

        await self.runner.setup()
        site = web.TCPSite(self.runner, self.config.host, self.config.port)
        await site.start()

    async def _load(self, path, mode="r", content_type="text/plain", content_modifier=None):

        # Read file
        contents = None
        async with aiofiles.open(path, mode=mode) as f:
            contents = await f.read()

        # Call modifier if it was passed
        if content_modifier:
            contents = content_modifier(contents)

        # Return web response
        return web.Response(body=contents, content_type=content_type)

    def _inject_script(self, contents):

        soup = BeautifulSoup(contents, "html.parser")
        if soup.head:
            script_tag = soup.new_tag("script")
            script_tag.string = self.injection_script
            soup.head.append(script_tag)
        contents = soup.prettify()
        return contents.encode("utf-8")

    def _open_browser(self):

        url = f"http://{self.config.host}:{self.config.port}/{self.config.index}"
        logger.debug(f"Opening browser at: {url}")
        webbrowser.open_new_tab(url)
