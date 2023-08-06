"""
Application context module.
"""
from contextvars import ContextVar
from dataclasses import dataclass

from .principal import Principal


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


ctx = ContextVar("ctx", default=AppContext(Principal.anonymous()))


def app_context() -> AppContext:
    """
    Get application context.
    """
    return ctx.get()
