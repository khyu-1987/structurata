from sdk.client import HunterClient
from sdk.models import VerifiedEmailRecord
from storages.base import BaseStorage

EMAIL_VALID_STATUS = 'valid'


class HunterService:

    def __init__(self, client: HunterClient, storage: BaseStorage[dict]) -> None:
        self.client = client
        self.storage = storage

    def save_verified_email_data(self, domain: str, first_name: str, last_name: str) -> None:
        find_data = self.client.find_email(domain, first_name, last_name).data
        if not find_data.email:
            return

        if not self._is_email_verified(find_data.email):
            return

        record = VerifiedEmailRecord(
            email=find_data.email,
            first_name=find_data.first_name,
            last_name=find_data.last_name,
            domain=find_data.domain,
            status=EMAIL_VALID_STATUS,
        )
        self.storage.create(key=find_data.email, record=record.model_dump())

    def _is_email_verified(self, email: str) -> bool:
        return self.client.verify_email(email).data.status == EMAIL_VALID_STATUS
