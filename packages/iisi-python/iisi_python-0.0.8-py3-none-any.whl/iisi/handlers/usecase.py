"""_summary_"""
import json
from dataclasses import dataclass
from typing import Any, Dict

import punq
from iisi.handlers.handler import AppHandler
from iisi.resolvers.usecase import UsecaseResolver


@dataclass
class UsecaseHandler(AppHandler):
    """_summary_"""

    usecase_resolver: UsecaseResolver
    routes: Dict
    container: punq.Container

    def handle(self, event: Dict[str, Any]):
        """
        Resolve request params

        :param event: The event to handle.
        """
        # Resolve params
        params = event.get("pathParameters", {}) | json.loads(event.get("body", "{}"))

        # Resolve handler
        usecase_module = self.routes[event.get("routeKey", "$default")]
        usecase_stack = self.usecase_resolver.resolve_usecase(usecase_module)

        self.container.register(usecase_stack.controller)
        self.container.register(usecase_stack.service)
        self.container.register(usecase_stack.repository_port, usecase_stack.repository)
        handler = self.container.resolve(usecase_stack.controller)

        # Execute handler
        return handler(**params)  # type: ignore
