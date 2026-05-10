from sdk.client import HunterClient
from storages.base import BaseStorage

EMAIL_VALID_STATUS = 'valid'


class HunterService:

    def __init__(self, client: HunterClient, storage: BaseStorage) -> None:
        self.client = client
        self.storage = storage

    def save_verified_email_data(self, domain: str, first_name: str, last_name: str) -> None:
        response_data = self.client.find_email(domain, first_name, last_name)
        email_data = response_data.get('data') or {}
        email = email_data.get('email')

        if email and self._is_email_verified(email):
            self.storage.create(key=email, record=email_data)

    def _is_email_verified(self, email: str) -> bool:
        response_data = self.client.verify_email(email)
        verification_data = response_data.get('data') or {}
        return verification_data.get('status') == EMAIL_VALID_STATUS
