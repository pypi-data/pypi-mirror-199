"""_summary_
"""
from dataclasses import dataclass
from typing import Type

from iisi.application.usecase import IController, IRepository, IService


@dataclass(frozen=True)
class UseCaseStack:
    """Represents a Iisi application use case implementation stack."""

    controller: Type[IController]
    service: Type[IService]
    repository_port: Type[IRepository]
    repository: Type[IRepository]
