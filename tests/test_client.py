from unittest.mock import MagicMock

import pytest
import requests
from pytest_mock import MockerFixture

from sdk.client import HunterClient
from sdk.exceptions import (
    HunterAPIError,
    HunterAuthError,
    HunterBadRequestError,
    HunterRateLimitError,
    HunterResponseError,
    HunterUnreachableError,
)
from sdk.models import FindEmailResponse, VerifyEmailResponse

STATUS_TO_EXCEPTION = (
    (401, HunterAuthError),
    (403, HunterAuthError),
    (429, HunterRateLimitError),
    (500, HunterUnreachableError),
    (400, HunterBadRequestError),
)


class TestHunterClient:

    def test_find_email(
        self,
        client: HunterClient,
        mocker: MockerFixture,
        find_email_response_json: dict,
        find_email_response: FindEmailResponse,
    ) -> None:
        mock_response = MagicMock(ok=True)
        mock_response.json.return_value = find_email_response_json
        mock_request = mocker.patch.object(
            client.session, "get", return_value=mock_response
        )

        response = client.find_email("reddit.com", "Alexis", "Ohanian")

        assert response == find_email_response
        mock_request.assert_called_once_with(
            "https://api.hunter.io/v2/email-finder",
            headers={"Authorization": "Bearer bla-bla-bla"},
            params={
                "domain": "reddit.com",
                "first_name": "Alexis",
                "last_name": "Ohanian",
            },
            timeout=10,
        )

    def test_verify_email(
        self,
        client: HunterClient,
        mocker: MockerFixture,
        verify_email_valid_response: VerifyEmailResponse,
    ) -> None:
        mock_response = MagicMock(ok=True)
        mock_response.json.return_value = {"data": {"status": "valid"}}
        mock_request = mocker.patch.object(
            client.session, "get", return_value=mock_response
        )

        response = client.verify_email("alexis@reddit.com")

        assert response == verify_email_valid_response
        mock_request.assert_called_once_with(
            "https://api.hunter.io/v2/email-verifier",
            headers={"Authorization": "Bearer bla-bla-bla"},
            params={"email": "alexis@reddit.com"},
            timeout=10,
        )


class TestHunterClientErrors:

    @pytest.mark.parametrize(("status_code", "expected_exc"), STATUS_TO_EXCEPTION)
    def test_error_status_raises_typed_exception(
        self,
        client: HunterClient,
        mocker: MockerFixture,
        status_code: int,
        expected_exc: type[HunterAPIError],
    ) -> None:
        mock_response = MagicMock(ok=False, status_code=status_code)
        mocker.patch.object(client.session, "get", return_value=mock_response)

        with pytest.raises(expected_exc):
            client.verify_email("alexis@reddit.com")

    def test_invalid_json_raises_response_error(
        self, client: HunterClient, mocker: MockerFixture
    ) -> None:
        mock_response = MagicMock(ok=True)
        mock_response.json.side_effect = ValueError("not json")
        mocker.patch.object(client.session, "get", return_value=mock_response)

        with pytest.raises(HunterResponseError):
            client.verify_email("alexis@reddit.com")

    def test_schema_mismatch_raises_response_error(
        self, client: HunterClient, mocker: MockerFixture
    ) -> None:
        mock_response = MagicMock(ok=True)
        mock_response.json.return_value = {"data": {}}
        mocker.patch.object(client.session, "get", return_value=mock_response)

        with pytest.raises(HunterResponseError):
            client.verify_email("alexis@reddit.com")

    def test_connection_error_raises_unreachable(
        self, client: HunterClient, mocker: MockerFixture
    ) -> None:
        mocker.patch.object(
            client.session,
            "get",
            side_effect=requests.exceptions.ConnectionError("dns failure"),
        )

        with pytest.raises(HunterUnreachableError):
            client.verify_email("alexis@reddit.com")
