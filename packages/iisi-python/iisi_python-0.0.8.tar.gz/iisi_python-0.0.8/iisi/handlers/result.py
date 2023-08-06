"""
Result handlers module.
"""
import json
from dataclasses import asdict, dataclass
from http import HTTPStatus
from typing import Any, Dict

from authoritah import NotAuthorized

from iisi.application.exception import DataException, NotAuthorizedException

from .handler import AppHandler


@dataclass
class HttpResultHandler(AppHandler):
    """
    Http result handler
    """

    def handle(self, event: Dict[str, Any]) -> Dict:
        """
        Handle result

        :param event: The event to handle.
        """
        try:
            return self._ok_response(event)
        except (ValueError, TypeError) as value_error:
            return self._response(HTTPStatus.BAD_REQUEST, str(value_error))
        except (NotAuthorized, NotAuthorizedException) as not_authorized:
            return self._response(HTTPStatus.UNAUTHORIZED, str(not_authorized))
        except DataException as repo_error:
            return self._response(HTTPStatus.INTERNAL_SERVER_ERROR, str(repo_error))
        except Exception as error:  # pylint: disable=broad-except
            return self._response(HTTPStatus.INTERNAL_SERVER_ERROR, str(error))

    def _ok_response(self, output: Any) -> Dict:
        """OK response."""
        body = (
            [asdict(item) for item in output]
            if isinstance(output, list)
            else asdict(output)
            if output is not None
            else None
        )
        return {
            "statusCode": HTTPStatus.OK,
            "headers": {"Content-Type": "application/json"},
            "body": json.dumps(body) if body is not None else None,
        }

    def _response(self, status_code: HTTPStatus, output: str) -> Dict:
        """Http status response."""
        body = output if output is not None else None
        return {
            "statusCode": status_code,
            "headers": {"Content-Type": "application/json"},
            "body": body,
        }


class CliResultHandler(AppHandler):
    """
    Cli result handler.

    :param AppHandler: _description_.
    """

    def handle(self, event: Dict[str, Any]) -> Dict:
        """
        Handle result as cli response.

        :param event: The event to handle.
        """
        try:
            self.ok_response(event)
        except (ValueError, TypeError) as value_error:
            self.error_response("Bad request:", value_error)
        except NotAuthorized as not_authorized:
            self.error_response("Not authorized:", not_authorized)
        except Exception as error:  # pylint: disable=broad-except
            self.error_response("Unknown error:", error)
        return event

    def ok_response(self, output: Any) -> None:
        """Print out ok response."""
        body = (
            [asdict(item) for item in output]
            if isinstance(output, list)
            else asdict(output)
            if output is not None
            else None
        )
        print("ok:" + str(body) if body is not None else "ok")

    def error_response(self, prefix: str, output: Any) -> None:
        """Print error out response."""
        print(prefix + str(asdict(output)) if output is not None else prefix)
