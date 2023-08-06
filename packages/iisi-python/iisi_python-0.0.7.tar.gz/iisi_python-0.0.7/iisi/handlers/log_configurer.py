"""
Logging configurator module.
"""
import logging
from dataclasses import dataclass
from typing import Any, Dict, List

from .handler import AppHandler


@dataclass
class LogConfigurator(AppHandler):
    """
    Event logging handler.
    """

    log_level: str
    error: List[str]

    def handle(self, event: Dict[str, Any]):
        """
        Configure logger.
        """
        if len(logging.getLogger().handlers) > 0:
            # The Lambda environment pre-configures a handler logging to stderr.
            # If a handler is already configured, `.basicConfig` does not execute.
            # Thus we set the level directly.
            logging.getLogger().setLevel(self.log_level)
        else:
            logging.basicConfig(level=self.log_level)

        for name in self.error:
            logging.getLogger(name).setLevel(logging.ERROR)
        return event
