"""
Authorization module.
"""
from authoritah import Authorizer

from .context import app_context
from .principal import Principal

auth = Authorizer(
    permissions={
        "admin": {
            "grants": [
                "application:create",
                "user:create",
                "user:update",
                "user:delete",
                "user:read",
            ]
        }
    }
)


@auth.identity_provider
def _identity() -> Principal:
    """Returns the current authenticated principal."""
    return app_context().principal


@auth.default_role_provider
def _roles(principal, _context=None):
    """Get roles for the current principal."""
    return principal.roles
