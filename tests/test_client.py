from unittest.mock import MagicMock

from pytest_mock import MockerFixture

from sdk.client import HunterClient


class TestHunterClient:

    def test_find_email(
        self,
        client: HunterClient,
        mocker: MockerFixture,
        find_email_response: dict,
    ) -> None:
        mock_response = MagicMock(ok=True)
        mock_response.json.return_value = find_email_response
        mock_request = mocker.patch('sdk.client.requests.get', return_value=mock_response)

        response_data = client.find_email('reddit.com', 'Alexis', 'Ohanian')

        assert response_data == find_email_response
        mock_request.assert_called_once_with(
            'https://api.hunter.io/v2/email-finder',
            headers={'Authorization': 'Bearer bla-bla-bla'},
            params={
                'domain': 'reddit.com',
                'first_name': 'Alexis',
                'last_name': 'Ohanian',
            },
            timeout=10,
        )

    def test_verify_email(
        self,
        client: HunterClient,
        mocker: MockerFixture,
        verify_email_valid_response: dict,
    ) -> None:
        mock_response = MagicMock(ok=True)
        mock_response.json.return_value = verify_email_valid_response
        mock_request = mocker.patch('sdk.client.requests.get', return_value=mock_response)

        response_data = client.verify_email('alexis@reddit.com')

        assert response_data == verify_email_valid_response
        mock_request.assert_called_once_with(
            'https://api.hunter.io/v2/email-verifier',
            headers={'Authorization': 'Bearer bla-bla-bla'},
            params={'email': 'alexis@reddit.com'},
            timeout=10,
        )
