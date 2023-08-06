"""
Event logging handler module.
"""
import logging
from dataclasses import dataclass
from typing import Any, Dict

from .handler import AppHandler

log = logging.getLogger(__name__)


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
