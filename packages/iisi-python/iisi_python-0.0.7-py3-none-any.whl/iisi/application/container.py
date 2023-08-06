"""_summary_
"""


from typing import Any, List

import punq


class UseCase:
    """_summary_"""


class Route:
    """Route value object."""


container = punq.Container()


class Container:
    """Iisi application dependency injection container."""

    @classmethod
    def register_usecase(cls, route: Route, usecase: UseCase):
        """_summary_"""

    @classmethod
    def register(cls, key: Any, implementation: Any, **kwargs):
        """_summary_"""
        container.register(key, implementation, **kwargs)

    @classmethod
    def resolve_all(cls, key: Any) -> List[Any]:
        """_summary_

        Args:
            key (Any): _description_

        Returns:
            List[Any]: _description_
        """
        return container.resolve_all(key)
