"""_summary_
"""
import logging as log
from dataclasses import dataclass
from typing import Any, Dict

from iisi.application.context import app_context
from iisi.application.exception import AuthenticationException
from iisi.application.principal import Principal

from .handler import AppHandler


@dataclass
class JwtPrincipalHandler(AppHandler):
    """Handle JWT token claims."""

    domain_name: str

    def handle(self, event: Dict[str, Any]):
        try:
            log.debug("%s: %s, domain: %s", self.__class__.__name__, event, self.domain_name)
            claims = event["requestContext"]["authorizer"]["jwt"]["claims"]
            app_context().principal = Principal.new(
                user_id=claims[f"{self.domain_name}/user_id"],
                customer_id=claims[f"{self.domain_name}/customer_id"],
                roles=claims[f"{self.domain_name}/roles"].lstrip("[").rstrip("[").split(),
            )
            return event
        except Exception as exc:
            log.exception(exc)
            raise AuthenticationException("Error handling jwt claims.") from exc
