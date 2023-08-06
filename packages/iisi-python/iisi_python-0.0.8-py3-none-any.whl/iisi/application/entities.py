"""
Domain entity
"""
from dataclasses import dataclass
from .value_objects import TenantId


@dataclass(frozen=True)
class Entity:
    """
    Domain entity.
    """

    tenant_id: TenantId
