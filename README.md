# Structurata

Find and verify an email via [Hunter.io](https://hunter.io/api-documentation/v2), then store it.

## Install

```bash
pip install -r requirements.txt
export HUNTER_API_KEY=your-key
```

## Use

```python
import config
from sdk.client import HunterClient
from sdk.service import HunterService
from storages.in_memory import InMemoryStorage

service = HunterService(HunterClient(config.HUNTER_API_KEY), InMemoryStorage())
service.save_verified_email_data(domain='reddit.com', first_name='Alexis', last_name='Ohanian')
```

## Checks

```bash
pytest
flake8 .
mypy .
```
