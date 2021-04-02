import time

from loguru import logger
from watchdog.observers import Observer
from watchdog.tricks import ShellCommandTrick

from .threaded import Threaded
from .events import Event


class Watcher(Threaded):
    def __init__(self, config, dispatcher) -> None:

        super().__init__()
        self.config = config
        self.dispatcher = dispatcher
        self.handler = FileChangeHandler(config, dispatcher)
        self.observer = Observer()
        for pathname in set(config.dirs):
            self.observer.schedule(self.handler, pathname, recursive=True)

    def start(self):

        logger.debug("Starting observer thread")
        self.observer.start()
        logger.debug("Observer thred started")

    def stop(self):

        logger.debug("Stopping observer thread")
        self.observer.stop()
        self.observer.join()
        logger.debug("Observer thread stopped")


class FileChangeHandler(ShellCommandTrick):
    def __init__(self, config, dispatcher):

        self.config = config
        self.dispatcher = dispatcher
        self.cooldown_timer = time.time()
        super().__init__(
            shell_command=config.command,
            patterns=config.patterns,
            ignore_patterns=config.ignore_patterns,
            ignore_directories=config.ignore_dirs,
            wait_for_process=True,
            drop_during_process=True,
        )

    def on_any_event(self, event):

        command_result = None

        timeout = time.time() - self.cooldown_timer
        if timeout < self.config.wait:
            logger.debug(
                f"Ignoring watcher event because less time passed then specified in cooldown: {timeout:.2f} < {self.config.wait:.2f}")
            return None

        # Report event processing
        logger.debug(f"Processing event {event}.")

        # Run shell command
        try:
            command_result = super().on_any_event(event)
        except Exception as e:
            logger.error(f"{e}")
        logger.debug(f"Shell command executed with result: {command_result}.")

        # Register file changed event
        self.dispatcher.report(Event.ShellCommandFinished)

        # Remember current time for cooldown timer
        self.cooldown_timer = time.time()

        return command_result
