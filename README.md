# Structurata

Find and verify an email via [Hunter.io](https://hunter.io/api-documentation/v2), then store it.

## Install

```bash
pip install -r requirements.txt
export HUNTER_API_KEY=your-key
```

## Use

Context manager (preferred):

```python
import config
from sdk.client import HunterClient
from sdk.services import (
    EmailFinder,
    EmailVerifier,
    VerifiedEmailRecorder,
    VerifiedEmailRunner,
)
from storages.in_memory import InMemoryStorage

with HunterClient(config.HUNTER_API_KEY) as client:
    runner = VerifiedEmailRunner(
        finder=EmailFinder(client),
        verifier=EmailVerifier(client),
        recorder=VerifiedEmailRecorder(InMemoryStorage()),
    )
    runner.run(domain='reddit.com', first_name='Alexis', last_name='Ohanian')
```

## Logging

The SDK logs to `sdk.services` at `INFO`. To see those logs, configure logging in your application:

```python
import logging
logging.basicConfig(level=logging.INFO)
logging.getLogger('sdk').setLevel(logging.INFO)
```

## Checks

```bash
pytest
flake8 .
mypy .
```
