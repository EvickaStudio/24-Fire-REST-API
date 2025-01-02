class FireAPIError(Exception):
    """Base exception for FireAPI errors."""

    pass


class APIRequestError(FireAPIError):
    """Raised when an API request fails due to an error in the request."""

    pass


class APIAuthenticationError(FireAPIError):
    """Raised when API authentication fails."""

    pass
