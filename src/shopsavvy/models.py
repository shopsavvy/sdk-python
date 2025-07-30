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
    
    product_id: str = Field(..., description="Unique product identifier")
    name: str = Field(..., description="Product name")
    brand: Optional[str] = Field(None, description="Product brand")
    category: Optional[str] = Field(None, description="Product category")
    image_url: Optional[str] = Field(None, description="Product image URL")
    barcode: Optional[str] = Field(None, description="Product barcode")
    asin: Optional[str] = Field(None, description="Amazon ASIN")
    model: Optional[str] = Field(None, description="Product model number")
    mpn: Optional[str] = Field(None, description="Manufacturer part number")
    description: Optional[str] = Field(None, description="Product description")
    identifiers: Optional[Dict[str, str]] = Field(
        None, description="Additional product identifiers"
    )


class Offer(BaseModel):
    """Product offer from a retailer"""
    
    offer_id: str = Field(..., description="Unique offer identifier")
    retailer: str = Field(..., description="Retailer name")
    price: float = Field(..., description="Offer price")
    currency: str = Field(default="USD", description="Price currency")
    availability: Literal["in_stock", "out_of_stock", "limited_stock"] = Field(
        ..., description="Product availability"
    )
    condition: Literal["new", "used", "refurbished"] = Field(
        ..., description="Product condition"
    )
    url: str = Field(..., description="Link to product page")
    shipping: Optional[float] = Field(None, description="Shipping cost")
    last_updated: str = Field(..., description="Last update timestamp")


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


class UsageInfo(BaseModel):
    """API usage information"""
    
    credits_used: int = Field(..., description="Credits used in current period")
    credits_remaining: int = Field(..., description="Credits remaining")
    credits_total: int = Field(..., description="Total credits for current period")
    billing_period_start: str = Field(..., description="Billing period start date")
    billing_period_end: str = Field(..., description="Billing period end date")
    plan_name: str = Field(..., description="Current subscription plan")


class APIResponse(BaseModel, Generic[T]):
    """Standard API response wrapper"""
    
    success: bool = Field(..., description="Whether request was successful")
    data: T = Field(..., description="Response data")
    message: Optional[str] = Field(None, description="Optional message")
    credits_used: Optional[int] = Field(None, description="Credits used for request")
    credits_remaining: Optional[int] = Field(
        None, description="Credits remaining after request"
    )


# Specific response types for convenience
ProductDetailsResponse = APIResponse[ProductDetails]
ProductDetailsBatchResponse = APIResponse[List[ProductDetails]]
OffersResponse = APIResponse[List[Offer]]
OffersBatchResponse = APIResponse[Dict[str, List[Offer]]]
PriceHistoryResponse = APIResponse[List[OfferWithHistory]]
SchedulingResponse = APIResponse[Dict[str, Union[bool, str]]]
SchedulingBatchResponse = APIResponse[List[Dict[str, Union[str, bool]]]]
ScheduledProductsResponse = APIResponse[List[ScheduledProduct]]
RemovalResponse = APIResponse[Dict[str, bool]]
RemovalBatchResponse = APIResponse[List[Dict[str, Union[str, bool]]]]
UsageResponse = APIResponse[UsageInfo]