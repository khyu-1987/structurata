class HunterAPIError(Exception):
    """Base class for any Hunter API failure"""


class HunterUnreachableError(HunterAPIError):
    """Network failure or server-side errors after retries"""


class HunterAuthError(HunterAPIError):
    """Bad or expired API key"""


class HunterRateLimitError(HunterAPIError):
    """Rate limit error"""


class HunterBadRequestError(HunterAPIError):
    """Bad client request"""


class HunterResponseError(HunterAPIError):
    """JSON response is unparseable or schema is incorrect"""
