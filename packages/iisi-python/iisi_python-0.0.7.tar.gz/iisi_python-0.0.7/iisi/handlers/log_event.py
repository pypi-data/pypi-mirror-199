"""
Event logging handler module.
"""
import logging as log
from dataclasses import dataclass
from typing import Any, Dict

from .handler import AppHandler


@dataclass
class LogEventHandler(AppHandler):
    """
    Event logging handler.
    """

    def handle(self, event: Dict[str, Any]):
        """
        Log given event.

        :param event: The event to handle.
        """
        log.debug("%s", event)
        return event
