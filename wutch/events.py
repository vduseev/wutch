from enum import Enum

from loguru import logger


class Event(Enum):
    ShellCommandFinished = 1


class EventDispatcher(list):
    def report(self, event):
        """Report new event."""

        self.append(event)
        logger.debug(f"New {event} event has been reported.")

    def claim(self, event):
        """Claim all events of certain type."""

        claimed = [e for e in self if e == event]
        unclaimed = [e for e in self if e != event]
        super().clear()
        super().extend(unclaimed)

        # Report to logs
        if claimed:
            logger.debug(
                f"{len(claimed)} {event} events have been claimed from the dispatcher."
            )

        return claimed
