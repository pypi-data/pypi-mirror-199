"""_summary_
"""


from typing import Any, List

import punq

from iisi.domain.route import Route
from iisi.domain.usecase import UseCase


class Container:
    """Iisi application dependency injection container."""

    container = punq.Container()

    def register_usecase(self, route: Route, usecase: UseCase):
        """_summary_"""

    def register(self, key: Any, implementation: Any, **kwargs):
        """_summary_"""
        self.container.register(key, implementation, **kwargs)

    def resolve_all(self, key: Any) -> List[Any]:
        """_summary_

        Args:
            key (Any): _description_

        Returns:
            List[Any]: _description_
        """
        return self.container.resolve_all(key)
