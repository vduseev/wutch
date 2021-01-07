import os
import threading
import time
from pathlib import Path
import importlib.resources as pkg_resources
from typing import Optional

from bs4 import BeautifulSoup
from loguru import logger

from .events import Event, EventDispatcher
from .config import Config
from . import js


class Injector:
    def __init__(
        self, config: Config, dispatcher: Optional[EventDispatcher] = None
    ) -> None:

        super().__init__()
        self.config = config
        self.dispatcher = dispatcher
        self.thread = threading.Thread(target=self._inject_forever)
        self.thread.daemon = True
        self.running = False
        self.lock = threading.Lock()

    def start(self, dispatcher: Optional[EventDispatcher] = None, thread_lock: threading.Lock = threading.Lock()):

        # Reassign lock
        self.lock = thread_lock

        # Reassign event dispatcher if it was passsed
        if dispatcher:
            self.dispatcher = dispatcher

        logger.debug("Starting injector thread")
        self.running = True
        self.thread.start()

    def stop(self):

        logger.debug("Stopping injector thread")
        self.running = False
        self.thread.join()

    def inject(self):

        logger.debug("Running inject operation")

        script_path = Path(self.config.js_dir) / "wutch.js"

        # Write down our javascript file
        self._inject_js(script_path)

        # Update html files with <script> tag inside <body> pointing
        # to our js script.
        self._inject_html(script_path)

        # Report event
        self.dispatcher.report(Event.JSInjectFinished)

    def _inject_js(self, script_path):

        # Read JS file
        script = pkg_resources.read_text(js, "wutch.js")

        host = self.config.host
        if host == "0.0.0.0":
            host = "localhost"
        port = self.config.port
        script = script.replace(
            "http://localhost:50231",
            f"http://{host}:{port}",
        )

        # Write it to the specified location
        script_path.write_text(script)

        # Log message
        logger.debug(f"JS file created at: {script_path}")

    def _inject_html(self, script_path):

        for dir in filter(
            lambda d: d.is_dir(),
            [Path(d) for d in self.config.build_dirs],
        ):
            for pattern in self.config.inject_patterns:
                for f in [x for x in dir.rglob(pattern) if x.is_file()]:

                    # Read HTML file
                    html_doc = f.read_text()

                    # Parse it
                    soup = BeautifulSoup(html_doc, "html.parser")

                    if soup.body:
                        # Add new JS function as a callback on body tag load
                        soup.body["onLoad"] = "wutch();"

                        # Find out relative position of the file to the script
                        common_path = Path(
                            os.path.commonpath([f, script_path])
                        )
                        relative_path = script_path.relative_to(common_path)

                        script_src = f"{relative_path}"
                        # Add new script tag to every file
                        if not soup.body.find_all("script", src=script_src):
                            # Only add new tag if hasn't yet been added to this html file
                            script_tag = soup.new_tag(
                                "script", src=script_src
                            )
                            soup.body.append(script_tag)
                            logger.debug(
                                f"Tag <script src='{script_src}' added to HTML at {f}"
                            )
                        else:
                            logger.debug(
                                f"HTML at {f} already contains proper <script src='{script_src}'> tag"
                            )

                        # Write file back
                        output = soup.prettify()
                        f.write_text(output)

                    else:
                        logger.debug(
                            f"HTML file without <body> rejected at {f}"
                        )

    def _inject_forever(self):

        logger.debug("Injector thread started")
        while self.running:
            if self.dispatcher.count(Event.ShellCommandFinished):
                with self.lock:
                    self.dispatcher.claim(Event.ShellCommandFinished)
                    self.inject()

            time.sleep(self.config.injector_cooldown)
        logger.debug("Injector thread stopped")
