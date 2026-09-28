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
    title_short: Optional[str] = Field(None, description="Shortened human-friendly title")
    slug: Optional[str] = Field(None, description="URL-friendly slug")
    description: Optional[str] = Field(None, description="Product description text")
    categories: Optional[List[str]] = Field(None, description="Category paths")
    attributes: Optional[Dict[str, str]] = Field(None, description="Product specifications (flat key-value)")
    rating: Optional[Dict[str, Any]] = Field(None, description="Aggregated rating with value and count")
    score: Optional[Dict[str, Any]] = Field(None, description="Expert quality scores on a 0-1 scale: overall, customer, professional, plus an 'aspects' dict keyed by free-form aspect names from the product's professional reviews")
    keywords: Optional[List[str]] = Field(None, description="Relevant search keywords")
    identifiers: Optional[Dict[str, Any]] = Field(None, description="All known product identifiers")

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
    history: Optional[List["PriceHistoryEntry"]] = Field(None, description="Price history")

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
    """
    Historical price data point.

    The timestamp field is ``timestamp``, matching the parent Offer's own ``timestamp``
    and the real wire shape (``{availability, price, currency, timestamp}``). Points
    arrive newest first; ``availability`` is omitted when unknown. Every SDK in the fleet
    declared it as ``date`` — a key the API has never sent — until 2026-08-10
    (ShopSavvy prospector-audit s28-t2-2 / s28-t2-3).
    """

    timestamp: str = Field(..., description="ISO-8601 timestamp of the observation")
    price: float = Field(..., description="Price at this observation")
    currency: Optional[str] = Field(None, description="The ISO 4217 currency the price is denominated in. Null on an archived point with no recorded currency — never assume a missing value means USD (ShopSavvy prospector-audit d5-t3-1).")
    availability: Optional[str] = Field(None, description="Availability at this observation")


class OfferWithHistory(Offer):
    """
    Offer with historical price data, nested under each product's ``offers`` in a
    ``get_price_history()`` response (see ``ProductWithPriceHistory``).

    This used to declare a required ``price_history`` field. The API has never sent a key
    by that name — history has always arrived under ``history`` — so with Pydantic v2 this
    model raised ``ValidationError: price_history Field required`` on EVERY successful 200
    response, surfacing to the caller as a raw stack trace rather than data.

    List-typed response fields default to empty rather than being required, so a future
    server-side rename can never again turn every call into an unhandled ValidationError.
    """

    history: List[PriceHistoryEntry] = Field(
        default_factory=list, description="Historical price data"
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

    request_id: Optional[str] = Field(None, description="Request identifier, quote it in support requests")
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


class ProductWithPriceHistory(ProductWithOffers):
    """
    One product in a ``get_price_history()`` response.

    ``GET /products/offers/history`` returns one entry PER PRODUCT — the same product
    fields as the products endpoint — with an ``offers`` list in which every offer carries
    its own ``history`` series. Until 1.4.0 this SDK typed ``data`` as a flat list of
    offers with a required ``id``, so every real 200 raised
    ``ValidationError: data.0.id Field required`` (the first key checked on a product).
    """

    offers: List[OfferWithHistory] = Field(  # type: ignore[assignment]
        default_factory=list,
        description="Offers at each retailer, each with its price history (newest point first)",
    )


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
PriceHistoryResponse = APIResponse[List[ProductWithPriceHistory]]
SchedulingResponse = APIResponse[Dict[str, Union[bool, str]]]
SchedulingBatchResponse = APIResponse[List[Dict[str, Union[str, bool]]]]
ScheduledProductsResponse = APIResponse[List[ScheduledProduct]]
RemovalResponse = APIResponse[Dict[str, bool]]
RemovalBatchResponse = APIResponse[List[Dict[str, Union[str, bool]]]]
UsageResponse = APIResponse[UsageInfo]


# Deal types

class DealGrade(BaseModel):
    """Expert deal grade"""
    letter: str = Field(..., description="Grade letter (A, B, C, D, F)")
    suffix: Optional[str] = Field(None, description="Grade suffix (+, -)")
    value: float = Field(..., description="Numeric grade value (0-1)")
    justification: Optional[str] = Field(None, description="Why this grade was assigned")


class DealPricing(BaseModel):
    """Deal pricing information"""
    current: float = Field(..., description="Current deal price")
    original: Optional[float] = Field(None, description="Original/MSRP price")
    currency: str = Field("USD", description="Price currency")


class DealVotes(BaseModel):
    """Community deal votes"""
    upvotes: int = Field(0)
    downvotes: int = Field(0)
    score: int = Field(0)


class DealTag(BaseModel):
    """Deal taxonomy tag"""
    slug: str
    display: str


class Deal(BaseModel):
    """A shopping deal with expert grading"""
    path: str
    title: str
    subtitle: Optional[str] = None
    description: Optional[str] = None
    emoji: Optional[str] = None
    grade: DealGrade
    pricing: DealPricing
    retailer: Dict[str, Any] = Field(default_factory=dict)
    product: Optional[str] = None
    url: str
    image: Optional[Dict[str, Any]] = None
    votes: DealVotes = Field(default_factory=DealVotes)
    comment_count: int = 0
    tags: Optional[List[DealTag]] = None
    product_scores: Optional[Dict[str, Any]] = None
    expires_at: Optional[str] = None
    created_at: str


class DealsPagination(BaseModel):
    """Deals pagination info"""
    total: int
    has_more: bool
    limit: int
    offset: int


class DealsResponse(BaseModel):
    """Response from deals endpoint"""
    success: bool
    deals: List[Deal]
    pagination: DealsPagination
    meta: Optional[APIMeta] = None


# Review types

class TLDRReview(BaseModel):
    """Expert TLDR product review"""
    slug: str
    headline: str
    pros: List[str] = Field(default_factory=list)
    cons: List[str] = Field(default_factory=list)
    bottom_line: str = ""
    # Expert quality scores on a 0-1 scale: overall, customer, professional,
    # plus an 'aspects' dict keyed by free-form aspect names from the
    # product's professional reviews (the set of aspects varies per product).
    scores: Optional[Dict[str, Any]] = None


class ReviewResponse(BaseModel):
    """Response from product reviews endpoint"""
    success: bool
    product: Dict[str, str]
    review: Optional[TLDRReview] = None
    meta: Optional[APIMeta] = None