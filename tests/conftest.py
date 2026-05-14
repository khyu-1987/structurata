import pytest

from sdk.client import HunterClient
from sdk.models import FindEmailResponse, VerifiedEmailRecord, VerifyEmailResponse
from sdk.services import (
    EmailFinder,
    EmailVerifier,
    VerifiedEmailRecorder,
    VerifiedEmailRunner,
)
from storages.in_memory import InMemoryStorage


@pytest.fixture
def storage() -> InMemoryStorage[dict]:
    return InMemoryStorage()


@pytest.fixture
def email_storage() -> InMemoryStorage[VerifiedEmailRecord]:
    return InMemoryStorage()


@pytest.fixture
def client() -> HunterClient:
    return HunterClient(api_key="bla-bla-bla")


@pytest.fixture
def finder(client: HunterClient) -> EmailFinder:
    return EmailFinder(client)


@pytest.fixture
def verifier(client: HunterClient) -> EmailVerifier:
    return EmailVerifier(client)


@pytest.fixture
def recorder(email_storage: InMemoryStorage[VerifiedEmailRecord]) -> VerifiedEmailRecorder:
    return VerifiedEmailRecorder(storage=email_storage)


@pytest.fixture
def runner(
    finder: EmailFinder,
    verifier: EmailVerifier,
    recorder: VerifiedEmailRecorder,
) -> VerifiedEmailRunner:
    return VerifiedEmailRunner(finder=finder, verifier=verifier, recorder=recorder)


@pytest.fixture
def find_email_response_json() -> dict:
    return {
        "data": {
            "email": "alexis@reddit.com",
            "first_name": "Alexis",
            "last_name": "Ohanian",
            "domain": "reddit.com",
        },
    }


@pytest.fixture
def find_email_response(find_email_response_json: dict) -> FindEmailResponse:
    return FindEmailResponse.model_validate(find_email_response_json)


@pytest.fixture
def verify_email_valid_response() -> VerifyEmailResponse:
    return VerifyEmailResponse.model_validate({"data": {"status": "valid"}})


@pytest.fixture
def verify_email_invalid_response() -> VerifyEmailResponse:
    return VerifyEmailResponse.model_validate({"data": {"status": "invalid"}})
