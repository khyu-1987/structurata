from pytest_mock import MockerFixture

from sdk.service import HunterService
from storages.in_memory import InMemoryStorage


class TestHunterService:

    def test_save_email_valid_ok(
        self,
        service: HunterService,
        storage: InMemoryStorage,
        mocker: MockerFixture,
        find_email_response: dict,
        verify_email_valid_response: dict,
    ) -> None:
        mocker.patch.object(service.client, 'find_email', return_value=find_email_response)
        mocker.patch.object(service.client, 'verify_email', return_value=verify_email_valid_response)

        service.save_verified_email_data('reddit.com', 'Alexis', 'Ohanian')

        assert storage.read('alexis@reddit.com') == find_email_response['data']

    def test_save_email_invalid_fail(
        self,
        service: HunterService,
        storage: InMemoryStorage,
        mocker: MockerFixture,
        find_email_response: dict,
        verify_email_invalid_response: dict,
    ) -> None:
        mocker.patch.object(service.client, 'find_email', return_value=find_email_response)
        mocker.patch.object(service.client, 'verify_email', return_value=verify_email_invalid_response)

        service.save_verified_email_data('reddit.com', 'Alexis', 'Ohanian')

        assert storage.read_all() == []
