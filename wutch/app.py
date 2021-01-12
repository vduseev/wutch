from loguru import logger

from .config import Config
from .server import Server
from .watcher import Watcher
from .events import Event, EventDispatcher
from .threaded import Threaded


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
            logger.info("Performing 'run' action")
            watcher = Watcher(self.config, self.dispatcher)
            server = Server(self.config, self.dispatcher)
            Threaded.run([watcher, server])

        elif action == "watch":
            logger.info("Performing 'watch' action")
            watcher = Watcher(self.config, self.dispatcher)
            Threaded.run([watcher])

        elif action == "serve":
            logger.info("Performing 'serve' action")
            server = Server(self.config, self.dispatcher)
            Threaded.run([server])

        else:
            logger.info(f"Unknown action: {action}")
            print(
                f"Unknown action: {action}. Please use one of {', '.join(self.config.actions)}."
            )
