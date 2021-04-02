from loguru import logger

from .config import Config
from .server import Server
from .watcher import Watcher
from .events import EventDispatcher
from .threaded import Threaded


class WutchApplication:
    def __init__(self) -> None:

        self.config = None
        self.dispatcher = EventDispatcher()

    def cli(self):

        # Initialize config (will parse arguments and throw SystemExit if
        # something like flag '--help' is used).
        self.config = Config()
        threads = []

        logger.configure()

        watcher = Watcher(self.config, self.dispatcher)
        threads.append(watcher)

        if not self.config.no_server:
            server = Server(self.config, self.dispatcher)
            threads.append(server)

        Threaded.run(threads)
