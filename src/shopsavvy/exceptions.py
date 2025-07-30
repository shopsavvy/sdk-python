"""
Exception classes for ShopSavvy Data API
"""


class ShopSavvyError(Exception):
    """Base exception for all ShopSavvy API errors"""
    pass


class APIError(ShopSavvyError):
    """General API error"""
    
    def __init__(self, message: str, status_code: int = None, response_data: dict = None):
        super().__init__(message)
        self.status_code = status_code
        self.response_data = response_data


class AuthenticationError(APIError):
    """Authentication failed (invalid API key, etc.)"""
    pass


class RateLimitError(APIError):
    """Rate limit exceeded"""
    pass


class NotFoundError(APIError):
    """Resource not found (product, etc.)"""
    pass


class ValidationError(APIError):
    """Request validation failed"""
    pass


class TimeoutError(ShopSavvyError):
    """Request timeout"""
    pass


class NetworkError(ShopSavvyError):
    """Network connection error"""
    pass