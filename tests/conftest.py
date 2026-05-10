import pytest

from sdk.client import HunterClient
from sdk.service import HunterService
from storages.in_memory import InMemoryStorage


@pytest.fixture
def storage() -> InMemoryStorage:
    return InMemoryStorage()


@pytest.fixture
def client() -> HunterClient:
    return HunterClient(api_key='bla-bla-bla')


@pytest.fixture
def service(client: HunterClient, storage: InMemoryStorage) -> HunterService:
    return HunterService(client=client, storage=storage)


@pytest.fixture
def find_email_response() -> dict:
    return {
        'data': {
            'email': 'alexis@reddit.com',
            'first_name': 'Alexis',
            'last_name': 'Ohanian',
        },
    }


@pytest.fixture
def verify_email_valid_response() -> dict:
    return {'data': {'status': 'valid'}}


@pytest.fixture
def verify_email_invalid_response() -> dict:
    return {'data': {'status': 'invalid'}}
