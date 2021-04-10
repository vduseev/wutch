import os
import sys
from pathlib import Path

from loguru import logger
import ilexconf

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

        # Load different config file if provided
        if self.config.config:
            path = Path(self.config.config)
            # Only load if it's a correct different file
            if path.is_file() and path != Path(Config.defaults.config) and path.name == "wutch.cfg":
                different_config = ilexconf.from_json(path)
                self.config.merge(different_config)

                # Change context directory
                directory = path.parent
                os.chdir(directory)

        logger.debug(self.config)

        threads = []

        level = self.config.verbosity[self.config.verbose]
        logger.remove()
        logger.add(sys.stderr, level=level)

        watcher = Watcher(self.config, self.dispatcher)
        threads.append(watcher)

        if not self.config.no_server:
            server = Server(self.config, self.dispatcher)
            threads.append(server)

        Threaded.run(threads)
