from dataclasses import dataclass

from iisi.application.usecase import IController, IRepository, IService


@dataclass(frozen=True)
class UseCaseStack:
    """Represents a Iisi application use case implementation stack."""

    controller: IController
    service: IService
    repository: IRepository
