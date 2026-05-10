import requests

API_BASE_URL = 'https://api.hunter.io/v2/'
API_EMAIL_FINDER_PATH = 'email-finder'
API_EMAIL_VERIFIER_PATH = 'email-verifier'
API_TIMEOUT = 10


class HunterClient:

    def __init__(self, api_key: str) -> None:
        self.api_key = api_key

    def find_email(self, domain: str, first_name: str, last_name: str) -> dict:
        url = f'{API_BASE_URL}{API_EMAIL_FINDER_PATH}'
        query_params = {
            'domain': domain,
            'first_name': first_name,
            'last_name': last_name,
        }
        return self._make_request(url, query_params)

    def verify_email(self, email: str) -> dict:
        url = f'{API_BASE_URL}{API_EMAIL_VERIFIER_PATH}'
        query_params = {'email': email}
        return self._make_request(url, query_params)

    def _make_request(self, url: str, query_params: dict) -> dict:
        headers = {'Authorization': f'Bearer {self.api_key}'}
        response = requests.get(url, headers=headers, params=query_params, timeout=API_TIMEOUT)
        response.raise_for_status()
        return response.json()
