import logging

from sdk.client import HunterClient
from sdk.models import FindEmailData, VerifiedEmailRecord
from storages.base import BaseStorage

logger = logging.getLogger(__name__)

EMAIL_VALID_STATUS = "valid"


class EmailFinder:

    def __init__(self, client: HunterClient) -> None:
        self.client = client

    def find(self, domain: str, first_name: str, last_name: str) -> FindEmailData:
        return self.client.find_email(domain, first_name, last_name).data


class EmailVerifier:

    def __init__(self, client: HunterClient) -> None:
        self.client = client

    def verify(self, email: str) -> str:
        return self.client.verify_email(email).data.status


class VerifiedEmailRecorder:

    def __init__(self, storage: BaseStorage[VerifiedEmailRecord]) -> None:
        self.storage = storage

    def record(self, record: VerifiedEmailRecord) -> None:
        self.storage.create(key=record.email, record=record)


class VerifiedEmailRunner:

    def __init__(
        self,
        finder: EmailFinder,
        verifier: EmailVerifier,
        recorder: VerifiedEmailRecorder,
    ) -> None:
        self.finder = finder
        self.verifier = verifier
        self.recorder = recorder

    def run(self, domain: str, first_name: str, last_name: str) -> None:
        find_data = self.finder.find(domain, first_name, last_name)
        if not find_data.email:
            logger.info("no email found for %s %s @ %s", first_name, last_name, domain)
            return

        status = self.verifier.verify(find_data.email)
        if status != EMAIL_VALID_STATUS:
            logger.info("email %s failed verification: %s", find_data.email, status)
            return

        self.recorder.record(
            VerifiedEmailRecord(
                email=find_data.email,
                first_name=find_data.first_name,
                last_name=find_data.last_name,
                domain=find_data.domain,
                status=status,
            )
        )
        logger.info("recorded verified email %s", find_data.email)
