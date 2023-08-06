"""_summary_"""
import importlib
import inspect
import logging as log
import os
import os.path
import pkgutil
from types import ModuleType
from typing import Type

from iisi.application.domain.usecasestack import UseCaseStack
from iisi.application.exception import ApplicationException
from iisi.application.usecase import IController, IPort, IRepository, IService


class UsecaseResolver:
    """_summary_"""

    def resolve_usecase(self, usecase_module: ModuleType) -> UseCaseStack:  # noqa: C901
        """_summary_"""
        try:
            controller: Type[IController]
            service: Type[IService]
            repository: Type[IRepository]
            repository_port: Type[IPort]

            package_path = os.path.dirname(usecase_module.__file__)  # type: ignore
            for module_info in pkgutil.iter_modules([package_path]):  # type: ignore
                usecase_module_name = usecase_module.__name__ + "." + module_info.name
                imported_usecase_module = importlib.import_module(usecase_module_name)
                for _, uc_class in inspect.getmembers(imported_usecase_module):
                    if inspect.isclass(uc_class) and uc_class.__module__ == usecase_module_name:
                        if issubclass(uc_class, IController):
                            controller = uc_class
                        if issubclass(uc_class, IService):
                            service = uc_class
                        if issubclass(uc_class, IRepository):
                            if len(uc_class.__subclasses__()) == 0:
                                repository = uc_class
                            if len(uc_class.__subclasses__()) > 0:
                                repository_port = uc_class  # type: ignore
            return UseCaseStack(controller, service, repository_port, repository)  # type: ignore
        except Exception as exc:
            log.exception(exc)
            raise ApplicationException(
                f"Error resolving usecase module ({str(usecase_module)})."
            ) from exc
