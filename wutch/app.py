import time
from threading import Lock

from loguru import logger
from .config import Config
from .server import Server
from .watcher import Watcher
from .events import Event, EventDispatcher
from .injector import Injector


class WutchApplication:
    def __init__(self) -> None:

        self.config = None
        self.dispatcher = EventDispatcher()

    def cli(self):

        # Initialize config (will parse arguments and throw SystemExit if
        # something like flag '--help' is used).
        self.config = Config()

        action = self.config.action
        if action == "run":
            self._run()
        elif action == "watch":
            self._watch()
        elif action == "serve":
            self._serve()
        elif action == "inject":
            self._inject()
        else:
            logger.info(f"Unknown action: {action}")
            print(
                f"Unknown action: {action}. Please use one of {', '.join(self.config.actions)}."
            )

    def _watch(self):

        logger.info("Performing 'watch' action")

        watcher = Watcher(self.config, self.dispatcher)
        try:
            watcher.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.debug("Stopping watcher on KeyboardInterrupt")
            watcher.stop()

    def _serve(self):

        logger.info("Performing 'serve' action")

        server = Server(self.config, self.dispatcher)
        try:
            server.start()
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            logger.debug("Stopping server on KeyboardInterrupt")
            server.stop()

    def _inject(self):

        logger.info("Performing 'inject' action")

        injector = Injector(self.config)
        injector.inject()

    def _run(self):

        logger.info("Performing 'run' action")

        # Initialize file watcher
        watcher = Watcher(self.config, self.dispatcher)

        # Initialize local HTTP server
        server = Server(self.config, self.dispatcher)

        # Initialize HTML injector
        injector = Injector(self.config, self.dispatcher)

        try:
            # Common thread lock for to keep watcher and injector threads
            # from interjecting with one another while messing with the
            # build directories.
            thread_lock = Lock()

            # Boot file watcher. It will begin looking for file changes
            # in the watched directories and running proper build command
            # in response. As a result of each change it will report new
            # event to the event dispatcher.
            watcher.start(thread_lock=thread_lock)
            # Boot HTTP server. On each GET request it will claim all
            # unclaimed rebuild events from event dispatcher and report
            # a 'changed' status to the requestor. If there are no events
            # to be claimed it will report 'unchanged'
            server.start()
            # Boot Injector thread
            injector.start(thread_lock=thread_lock)
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.debug("Stopping all threads on KeyboardInterrupt")

        except Exception as ex:
            logger.error(f"{ex}")

        finally:
            watcher.stop()
            server.stop()
            injector.stop()

