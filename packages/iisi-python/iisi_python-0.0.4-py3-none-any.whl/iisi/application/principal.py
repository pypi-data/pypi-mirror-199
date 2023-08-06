"""_summary_
"""
from dataclasses import dataclass
from typing import List

from iisi.application.value_objects import CustomerId, MaxLengthString, PrincipalId

_ANONYMOUS_PRINCIPAL_ID = PrincipalId("00000000-0000-0000-0000-000000000001")
_ANONYMOUS_CUSTOMER_ID = CustomerId("00000000-0000-0000-0000-000000000001")


class Role(MaxLengthString):
    """
    Role value object.
    """

    max_length = 12


@dataclass(frozen=True)
class Principal:
    """Application principal."""

    id: PrincipalId
    customer_id: CustomerId
    roles: List[Role]

    @staticmethod
    def anonymous() -> "Principal":
        """Factory method for anonymous principal."""
        return Principal(id=_ANONYMOUS_PRINCIPAL_ID, customer_id=_ANONYMOUS_CUSTOMER_ID, roles=[])

    @staticmethod
    def new(user_id: str, customer_id: str, roles: List[str]) -> "Principal":
        """
        Factory method for constructing a user.
        """
        return Principal(
            id=PrincipalId(user_id),
            customer_id=CustomerId(customer_id),
            roles=[Role(role) for role in roles],
        )
