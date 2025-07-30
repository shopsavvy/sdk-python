"""
Official Python SDK for ShopSavvy Data API

This package provides a convenient interface to interact with the ShopSavvy Data API,
allowing you to access product data, pricing information, and price history
across thousands of retailers and millions of products.

For more information, visit: https://shopsavvy.com/data
"""

from .client import ShopSavvyDataAPI, create_client
from .models import (
    ProductDetails,
    Offer,
    PriceHistoryEntry,
    OfferWithHistory,
    ScheduledProduct,
    UsageInfo,
    APIResponse,
    ShopSavvyConfig,
)
from .exceptions import (
    ShopSavvyError,
    APIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

__version__ = "1.0.0"
__author__ = "ShopSavvy by Monolith Technologies, Inc."
__email__ = "business@shopsavvy.com"

__all__ = [
    # Main client
    "ShopSavvyDataAPI",
    "create_client",
    # Models
    "ProductDetails",
    "Offer",
    "PriceHistoryEntry", 
    "OfferWithHistory",
    "ScheduledProduct",
    "UsageInfo",
    "APIResponse",
    "ShopSavvyConfig",
    # Exceptions
    "ShopSavvyError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
]