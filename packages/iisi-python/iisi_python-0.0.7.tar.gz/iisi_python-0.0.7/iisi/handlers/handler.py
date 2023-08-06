"""
Event handler module.
"""
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Any, Dict


@dataclass
class AppHandler(ABC):
    """
    Application event handler
    """

    @abstractmethod
    def handle(self, event: Dict[str, Any]) -> Dict:
        """_summary_"""
        raise NotImplementedError(f"{type(self).__name__} not implemented.")
