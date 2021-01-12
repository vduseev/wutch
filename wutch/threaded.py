import time
from typing import List

from loguru import logger


class Threaded:
    
    def start(self):
        """Start the thread."""

    def stop(self):
        """Stop the thread."""

    @staticmethod
    def run(runnables: List["Threaded"]):

        try:
            # Start all threads
            for r in runnables:
                r.start()

            # Sleep indefinitely
            while True:
                time.sleep(1)

        except KeyboardInterrupt:
            logger.debug("Stopping all threads on KeyboardInterrupt")

        except Exception as ex:
            logger.error(f"{ex}")

        finally:
            # Stopping all threads
            for r in runnables:
                r.stop()
