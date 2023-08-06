"""
Application context module.
"""
import logging
from contextvars import ContextVar
from dataclasses import asdict, dataclass

from .principal import Principal

log = logging.getLogger(__name__)


@dataclass
class AppContext:
    """Application context."""

    _principal: Principal

    @property
    def principal(self) -> Principal:
        """
        Get application context principal.

        :return: principal: _description_.
        """
        return self._principal

    @principal.setter
    def principal(self, principal: Principal) -> None:
        self._principal = principal
        ctx.set(self)
        log.debug("App context principal set to: %s", asdict(principal))


ctx = ContextVar("ctx", default=AppContext(_principal=Principal.anonymous()))


def app_context() -> AppContext:
    """
    Get application context.
    """
    return ctx.get()
