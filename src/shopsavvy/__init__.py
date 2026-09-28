"""
Official Python SDK for ShopSavvy Data API

This package provides a convenient interface to interact with the ShopSavvy Data API,
allowing you to access product data, pricing information, and price history
across thousands of retailers and millions of products.

For more information, visit: https://shopsavvy.com/data
"""

from ._version import __version__
from .client import ShopSavvyDataAPI, create_client
from .models import (
    ProductDetails,
    Offer,
    PriceHistoryEntry,
    OfferWithHistory,
    ProductWithOffers,
    ProductWithPriceHistory,
    APIMeta,
    ScheduledProduct,
    UsageInfo,
    APIResponse,
    MessageResponse,
    ShopSavvyConfig,
    Deal,
    DealGrade,
    DealPricing,
    DealVotes,
    DealsResponse,
    TLDRReview,
    ReviewResponse,
)
from .exceptions import (
    ShopSavvyError,
    APIError,
    AuthenticationError,
    RateLimitError,
    NotFoundError,
    ValidationError,
)

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
    "ProductWithOffers",
    "ProductWithPriceHistory",
    "APIMeta",
    "ScheduledProduct",
    "UsageInfo",
    "APIResponse",
    "MessageResponse",
    "ShopSavvyConfig",
    "Deal",
    "DealGrade",
    "DealPricing",
    "DealVotes",
    "DealsResponse",
    "TLDRReview",
    "ReviewResponse",
    # Exceptions
    "ShopSavvyError",
    "APIError",
    "AuthenticationError",
    "RateLimitError",
    "NotFoundError",
    "ValidationError",
]