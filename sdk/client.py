from http import HTTPStatus
from types import TracebackType
from typing import Any, Self, TypeVar

import requests
from pydantic import BaseModel, ValidationError
from requests.adapters import HTTPAdapter
from urllib3.util.retry import Retry

from sdk.exceptions import (
    HunterAPIError,
    HunterAuthError,
    HunterBadRequestError,
    HunterRateLimitError,
    HunterResponseError,
    HunterUnreachableError,
)
from sdk.models import FindEmailResponse, VerifyEmailResponse

API_BASE_URL = "https://api.hunter.io/v2/"
API_EMAIL_FINDER_PATH = "email-finder"
API_EMAIL_VERIFIER_PATH = "email-verifier"
API_TIMEOUT_SECONDS = 10
RETRY_TOTAL = 3
RETRY_BACKOFF_FACTOR = 0.5
RETRYABLE_STATUS_CODES = (
    HTTPStatus.TOO_MANY_REQUESTS,
    HTTPStatus.INTERNAL_SERVER_ERROR,
    HTTPStatus.BAD_GATEWAY,
    HTTPStatus.SERVICE_UNAVAILABLE,
    HTTPStatus.GATEWAY_TIMEOUT,
)
AUTH_FAILURE_CODES = (
    HTTPStatus.UNAUTHORIZED,
    HTTPStatus.FORBIDDEN,
)

ResponseModel = TypeVar("ResponseModel", bound=BaseModel)


def _build_session() -> requests.Session:
    session = requests.Session()
    retry = Retry(
        total=RETRY_TOTAL,
        backoff_factor=RETRY_BACKOFF_FACTOR,
        status_forcelist=RETRYABLE_STATUS_CODES,
        allowed_methods=("GET",),
        raise_on_status=False,
    )
    session.mount("https://", HTTPAdapter(max_retries=retry))
    return session


def _exception_for_status(status: int) -> type[HunterAPIError]:
    if status in AUTH_FAILURE_CODES:
        return HunterAuthError
    if status == HTTPStatus.TOO_MANY_REQUESTS:
        return HunterRateLimitError
    if status >= HTTPStatus.INTERNAL_SERVER_ERROR:
        return HunterUnreachableError
    return HunterBadRequestError


def _raise_for_status(response: requests.Response) -> None:
    if response.ok:
        return
    status = response.status_code
    raise _exception_for_status(status)(f"HTTP {status}")


def _parse_response(
    payload: dict[str, Any], model: type[ResponseModel]
) -> ResponseModel:
    try:
        return model.model_validate(payload)
    except ValidationError as exc:
        raise HunterResponseError(f"response schema: {exc}") from exc


class HunterClient:

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key
        self.session = _build_session()

    def __enter__(self) -> Self:
        return self

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc_val: BaseException | None,
        exc_tb: TracebackType | None,
    ) -> None:
        self.close()

    def close(self) -> None:
        self.session.close()

    def find_email(
        self, domain: str, first_name: str, last_name: str
    ) -> FindEmailResponse:
        url = f"{API_BASE_URL}{API_EMAIL_FINDER_PATH}"
        query_params = {
            "domain": domain,
            "first_name": first_name,
            "last_name": last_name,
        }
        return _parse_response(self._make_request(url, query_params), FindEmailResponse)

    def verify_email(self, email: str) -> VerifyEmailResponse:
        url = f"{API_BASE_URL}{API_EMAIL_VERIFIER_PATH}"
        query_params = {"email": email}
        return _parse_response(
            self._make_request(url, query_params), VerifyEmailResponse
        )

    def _make_request(self, url: str, query_params: dict) -> dict[str, Any]:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        try:
            response = self.session.get(
                url, headers=headers, params=query_params, timeout=API_TIMEOUT_SECONDS
            )
        except requests.exceptions.RequestException as exc:
            raise HunterUnreachableError(f"server is unreachable: {exc}") from exc

        _raise_for_status(response)

        try:
            return response.json()
        except ValueError as json_exc:
            raise HunterResponseError(f"invalid JSON: {json_exc}") from json_exc
