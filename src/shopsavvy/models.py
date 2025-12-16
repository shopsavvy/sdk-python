"""
Data models for ShopSavvy Data API
"""

from datetime import datetime
from typing import Any, Dict, Generic, List, Literal, Optional, TypeVar, Union

from pydantic import BaseModel, Field, validator

T = TypeVar("T")


class ShopSavvyConfig(BaseModel):
    """Configuration for ShopSavvy Data API client"""
    
    api_key: str = Field(..., description="ShopSavvy API key")
    base_url: str = Field(
        default="https://api.shopsavvy.com/v1", 
        description="Base URL for the API"
    )
    timeout: float = Field(default=30.0, description="Request timeout in seconds")

    @validator("api_key")
    def validate_api_key(cls, v: str) -> str:
        if not v:
            raise ValueError("API key is required")
        if not v.startswith(("ss_live_", "ss_test_")):
            raise ValueError(
                "Invalid API key format. API keys should start with ss_live_ or ss_test_"
            )
        return v


class ProductDetails(BaseModel):
    """Product details from ShopSavvy API"""

    # Core fields (matching API response)
    title: str = Field(..., description="Product title")
    shopsavvy: str = Field(..., description="ShopSavvy product ID")
    brand: Optional[str] = Field(None, description="Product brand")
    category: Optional[str] = Field(None, description="Product category")
    images: Optional[List[str]] = Field(None, description="Product image URLs")
    barcode: Optional[str] = Field(None, description="Product barcode")
    amazon: Optional[str] = Field(None, description="Amazon ASIN")
    model: Optional[str] = Field(None, description="Product model number")
    mpn: Optional[str] = Field(None, description="Manufacturer part number")
    color: Optional[str] = Field(None, description="Product color")

    # Convenience aliases
    @property
    def name(self) -> str:
        """Alias for title"""
        return self.title

    @property
    def product_id(self) -> str:
        """Alias for shopsavvy"""
        return self.shopsavvy

    @property
    def asin(self) -> Optional[str]:
        """Alias for amazon"""
        return self.amazon

    @property
    def image_url(self) -> Optional[str]:
        """First image URL for convenience"""
        return self.images[0] if self.images else None


class Offer(BaseModel):
    """Product offer from a retailer"""

    # Core fields (matching API response)
    id: str = Field(..., description="Unique offer identifier")
    retailer: Optional[str] = Field(None, description="Retailer name")
    price: Optional[float] = Field(None, description="Offer price")
    currency: Optional[str] = Field(None, description="Price currency")
    availability: Optional[str] = Field(None, description="Product availability")
    condition: Optional[str] = Field(None, description="Product condition")
    URL: Optional[str] = Field(None, description="Link to product page")
    seller: Optional[str] = Field(None, description="Marketplace seller name")
    timestamp: Optional[str] = Field(None, description="Last update timestamp")
    history: Optional[List[dict]] = Field(None, description="Price history")

    # Convenience aliases
    @property
    def offer_id(self) -> str:
        """Alias for id"""
        return self.id

    @property
    def url(self) -> Optional[str]:
        """Alias for URL"""
        return self.URL

    @property
    def last_updated(self) -> Optional[str]:
        """Alias for timestamp"""
        return self.timestamp


class PriceHistoryEntry(BaseModel):
    """Historical price data point"""
    
    date: str = Field(..., description="Date of price point")
    price: float = Field(..., description="Price on this date")
    availability: str = Field(..., description="Availability on this date")


class OfferWithHistory(Offer):
    """Offer with historical price data"""
    
    price_history: List[PriceHistoryEntry] = Field(
        ..., description="Historical price data"
    )


class ScheduledProduct(BaseModel):
    """Scheduled product monitoring information"""
    
    product_id: str = Field(..., description="Product identifier")
    identifier: str = Field(..., description="Original identifier used")
    frequency: Literal["hourly", "daily", "weekly"] = Field(
        ..., description="Monitoring frequency"
    )
    retailer: Optional[str] = Field(None, description="Specific retailer to monitor")
    created_at: str = Field(..., description="Schedule creation timestamp")
    last_refreshed: Optional[str] = Field(
        None, description="Last refresh timestamp"
    )


class UsagePeriod(BaseModel):
    """Current billing period usage details"""

    start_date: str = Field(..., description="Period start date")
    end_date: str = Field(..., description="Period end date")
    credits_used: int = Field(..., description="Credits used in current period")
    credits_limit: int = Field(..., description="Total credits limit for period")
    credits_remaining: int = Field(..., description="Credits remaining")
    requests_made: int = Field(..., description="Number of requests made")


class UsageInfo(BaseModel):
    """API usage information"""

    current_period: UsagePeriod = Field(..., description="Current billing period details")
    usage_percentage: int = Field(..., description="Percentage of credits used")

    # Convenience properties
    @property
    def credits_used(self) -> int:
        """Credits used in current period"""
        return self.current_period.credits_used

    @property
    def credits_remaining(self) -> int:
        """Credits remaining"""
        return self.current_period.credits_remaining

    @property
    def credits_total(self) -> int:
        """Total credits for current period"""
        return self.current_period.credits_limit

    @property
    def billing_period_start(self) -> str:
        """Billing period start date"""
        return self.current_period.start_date

    @property
    def billing_period_end(self) -> str:
        """Billing period end date"""
        return self.current_period.end_date


class PaginationInfo(BaseModel):
    """Pagination information for search results"""

    total: int = Field(..., description="Total number of results")
    limit: int = Field(..., description="Maximum results per page")
    offset: int = Field(..., description="Offset from start of results")
    returned: int = Field(..., description="Number of results in this response")


class APIMeta(BaseModel):
    """API response metadata"""

    credits_used: int = Field(0, description="Credits used for request")
    credits_remaining: int = Field(0, description="Credits remaining after request")
    rate_limit_remaining: Optional[int] = Field(None, description="Rate limit remaining")


class ProductSearchResult(BaseModel):
    """Product search results with pagination"""

    success: bool = Field(..., description="Whether request was successful")
    data: List[ProductDetails] = Field(..., description="Search result products")
    pagination: PaginationInfo = Field(..., description="Pagination metadata")
    meta: Optional[APIMeta] = Field(None, description="Response metadata")

    # Convenience properties
    @property
    def credits_used(self) -> int:
        """Credits used for this request"""
        return self.meta.credits_used if self.meta else 0

    @property
    def credits_remaining(self) -> int:
        """Credits remaining after this request"""
        return self.meta.credits_remaining if self.meta else 0


class ProductWithOffers(ProductDetails):
    """Product with nested offers (returned by offers endpoint)"""

    offers: List[Offer] = Field(default_factory=list, description="Product offers")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""

    success: bool = Field(..., description="Whether request was successful")
    data: T = Field(..., description="Response data")
    meta: Optional[APIMeta] = Field(None, description="Response metadata")
    message: Optional[str] = Field(None, description="Optional message")

    # Convenience properties
    @property
    def credits_used(self) -> int:
        """Credits used for this request"""
        return self.meta.credits_used if self.meta else 0

    @property
    def credits_remaining(self) -> int:
        """Credits remaining after this request"""
        return self.meta.credits_remaining if self.meta else 0


# Specific response types for convenience
ProductDetailsResponse = APIResponse[List[ProductDetails]]
ProductDetailsBatchResponse = APIResponse[List[ProductDetails]]
ProductSearchResponse = ProductSearchResult
OffersResponse = APIResponse[List[ProductWithOffers]]
OffersBatchResponse = APIResponse[Dict[str, List[Offer]]]
PriceHistoryResponse = APIResponse[List[OfferWithHistory]]
SchedulingResponse = APIResponse[Dict[str, Union[bool, str]]]
SchedulingBatchResponse = APIResponse[List[Dict[str, Union[str, bool]]]]
ScheduledProductsResponse = APIResponse[List[ScheduledProduct]]
RemovalResponse = APIResponse[Dict[str, bool]]
RemovalBatchResponse = APIResponse[List[Dict[str, Union[str, bool]]]]
UsageResponse = APIResponse[UsageInfo]