from pytest_mock import MockerFixture

from sdk.models import FindEmailResponse, VerifyEmailResponse
from sdk.service import VerifiedEmailRunner
from storages.in_memory import InMemoryStorage


class TestVerifiedEmailRunner:

    def test_run_email_valid_ok(
        self,
        runner: VerifiedEmailRunner,
        storage: InMemoryStorage[dict],
        mocker: MockerFixture,
        find_email_response: FindEmailResponse,
        verify_email_valid_response: VerifyEmailResponse,
    ) -> None:
        mocker.patch.object(
            runner.finder.client, "find_email", return_value=find_email_response
        )
        mocker.patch.object(
            runner.verifier.client,
            "verify_email",
            return_value=verify_email_valid_response,
        )

        runner.run("reddit.com", "Alexis", "Ohanian")

        assert storage.read("alexis@reddit.com") == {
            "email": "alexis@reddit.com",
            "first_name": "Alexis",
            "last_name": "Ohanian",
            "domain": "reddit.com",
            "status": "valid",
        }

    def test_run_email_invalid_fail(
        self,
        runner: VerifiedEmailRunner,
        storage: InMemoryStorage[dict],
        mocker: MockerFixture,
        find_email_response: FindEmailResponse,
        verify_email_invalid_response: VerifyEmailResponse,
    ) -> None:
        mocker.patch.object(
            runner.finder.client, "find_email", return_value=find_email_response
        )
        mocker.patch.object(
            runner.verifier.client,
            "verify_email",
            return_value=verify_email_invalid_response,
        )

        runner.run("reddit.com", "Alexis", "Ohanian")

        assert storage.read_all() == []

    def test_run_no_email_found_skips_verify_and_save(
        self,
        runner: VerifiedEmailRunner,
        storage: InMemoryStorage[dict],
        mocker: MockerFixture,
    ) -> None:
        empty_response = FindEmailResponse.model_validate({"data": {"email": None}})
        find_mock = mocker.patch.object(
            runner.finder.client, "find_email", return_value=empty_response
        )
        verify_mock = mocker.patch.object(runner.verifier.client, "verify_email")

        runner.run("reddit.com", "Alexis", "Ohanian")

        find_mock.assert_called_once()
        verify_mock.assert_not_called()
        assert storage.read_all() == []
