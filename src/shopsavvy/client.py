"""
ShopSavvy Data API Client
"""

import asyncio
from typing import Dict, List, Literal, Optional, Union
from urllib.parse import urlencode

import httpx

from .exceptions import (
    APIError,
    AuthenticationError,
    NetworkError,
    NotFoundError,
    RateLimitError,
    TimeoutError,
    ValidationError,
)
from .models import (
    APIResponse,
    Offer,
    OfferWithHistory,
    ProductDetails,
    ScheduledProduct,
    ShopSavvyConfig,
    UsageInfo,
)


class ShopSavvyDataAPI:
    """
    Official Python client for ShopSavvy Data API
    
    Provides access to product data, pricing information, and price history
    across thousands of retailers and millions of products.
    
    Args:
        config: Configuration object with API key and optional settings
        
    Example:
        >>> from shopsavvy import ShopSavvyDataAPI, ShopSavvyConfig
        >>> 
        >>> config = ShopSavvyConfig(api_key="ss_live_your_api_key_here")
        >>> api = ShopSavvyDataAPI(config)
        >>> 
        >>> # Look up a product
        >>> product = api.get_product_details("012345678901")
        >>> print(product.data.name)
    """
    
    def __init__(self, config: Union[ShopSavvyConfig, dict]):
        if isinstance(config, dict):
            config = ShopSavvyConfig(**config)
        
        self.config = config
        self._client = httpx.Client(
            base_url=config.base_url,
            timeout=config.timeout,
            headers={
                "Authorization": f"Bearer {config.api_key}",
                "Content-Type": "application/json",
                "User-Agent": "ShopSavvy-Python-SDK/1.0.0",
            },
        )
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.close()
    
    def close(self):
        """Close the HTTP client"""
        self._client.close()
    
    def _make_request(
        self, 
        method: str, 
        endpoint: str, 
        params: Optional[Dict] = None,
        json_data: Optional[Dict] = None
    ) -> Dict:
        """Make HTTP request and handle errors"""
        try:
            response = self._client.request(
                method=method,
                url=endpoint,
                params=params,
                json=json_data,
            )
            
            # Handle HTTP errors
            if response.status_code == 401:
                raise AuthenticationError(
                    "Authentication failed. Check your API key.",
                    status_code=response.status_code
                )
            elif response.status_code == 404:
                raise NotFoundError(
                    "Resource not found",
                    status_code=response.status_code
                )
            elif response.status_code == 429:
                raise RateLimitError(
                    "Rate limit exceeded. Please slow down your requests.",
                    status_code=response.status_code
                )
            elif response.status_code == 422:
                raise ValidationError(
                    "Request validation failed. Check your parameters.",
                    status_code=response.status_code
                )
            elif not response.is_success:
                try:
                    error_data = response.json()
                    error_message = error_data.get("error", f"HTTP {response.status_code}")
                except:
                    error_message = f"HTTP {response.status_code}: {response.text}"
                
                raise APIError(
                    error_message,
                    status_code=response.status_code,
                    response_data=error_data if 'error_data' in locals() else None
                )
            
            return response.json()
            
        except httpx.TimeoutException:
            raise TimeoutError(f"Request timeout after {self.config.timeout} seconds")
        except httpx.NetworkError as e:
            raise NetworkError(f"Network error: {str(e)}")
        except httpx.HTTPError as e:
            raise APIError(f"HTTP error: {str(e)}")
    
    def get_product_details(
        self, 
        identifier: str, 
        format: Optional[Literal["json", "csv"]] = None
    ) -> APIResponse[ProductDetails]:
        """
        Look up product details by identifier
        
        Args:
            identifier: Product identifier (barcode, ASIN, URL, model number, or ShopSavvy product ID)
            format: Response format (json or csv)
            
        Returns:
            Product details
            
        Example:
            >>> product = api.get_product_details("012345678901")
            >>> print(product.data.name)
        """
        params = {"identifier": identifier}
        if format:
            params["format"] = format
        
        response_data = self._make_request("GET", "/products/details", params=params)
        return APIResponse[ProductDetails](**response_data)
    
    def get_product_details_batch(
        self, 
        identifiers: List[str], 
        format: Optional[Literal["json", "csv"]] = None
    ) -> APIResponse[List[ProductDetails]]:
        """
        Look up details for multiple products
        
        Args:
            identifiers: List of product identifiers
            format: Response format (json or csv)
            
        Returns:
            List of product details
            
        Example:
            >>> products = api.get_product_details_batch(["012345678901", "B08N5WRWNW"])
            >>> for product in products.data:
            ...     print(product.name)
        """
        params = {"identifiers": ",".join(identifiers)}
        if format:
            params["format"] = format
        
        response_data = self._make_request("GET", "/products/details", params=params)
        return APIResponse[List[ProductDetails]](**response_data)
    
    def get_current_offers(
        self,
        identifier: str,
        retailer: Optional[str] = None,
        format: Optional[Literal["json", "csv"]] = None
    ) -> APIResponse[List[Offer]]:
        """
        Get current offers for a product
        
        Args:
            identifier: Product identifier
            retailer: Optional retailer to filter by
            format: Response format (json or csv)
            
        Returns:
            Current offers
            
        Example:
            >>> offers = api.get_current_offers("012345678901")
            >>> for offer in offers.data:
            ...     print(f"{offer.retailer}: ${offer.price}")
        """
        params = {"identifier": identifier}
        if retailer:
            params["retailer"] = retailer
        if format:
            params["format"] = format
        
        response_data = self._make_request("GET", "/products/offers", params=params)
        return APIResponse[List[Offer]](**response_data)
    
    def get_current_offers_batch(
        self,
        identifiers: List[str],
        retailer: Optional[str] = None,
        format: Optional[Literal["json", "csv"]] = None
    ) -> APIResponse[Dict[str, List[Offer]]]:
        """
        Get current offers for multiple products
        
        Args:
            identifiers: List of product identifiers
            retailer: Optional retailer to filter by
            format: Response format (json or csv)
            
        Returns:
            Dictionary mapping identifiers to their offers
        """
        params = {"identifiers": ",".join(identifiers)}
        if retailer:
            params["retailer"] = retailer
        if format:
            params["format"] = format
        
        response_data = self._make_request("GET", "/products/offers", params=params)
        return APIResponse[Dict[str, List[Offer]]](**response_data)
    
    def get_price_history(
        self,
        identifier: str,
        start_date: str,
        end_date: str,
        retailer: Optional[str] = None,
        format: Optional[Literal["json", "csv"]] = None
    ) -> APIResponse[List[OfferWithHistory]]:
        """
        Get price history for a product
        
        Args:
            identifier: Product identifier
            start_date: Start date (YYYY-MM-DD format)
            end_date: End date (YYYY-MM-DD format)
            retailer: Optional retailer to filter by
            format: Response format (json or csv)
            
        Returns:
            Offers with price history
            
        Example:
            >>> history = api.get_price_history("012345678901", "2024-01-01", "2024-01-31")
            >>> for offer in history.data:
            ...     print(f"{offer.retailer}: {len(offer.price_history)} price points")
        """
        params = {
            "identifier": identifier,
            "start_date": start_date,
            "end_date": end_date,
        }
        if retailer:
            params["retailer"] = retailer
        if format:
            params["format"] = format
        
        response_data = self._make_request("GET", "/products/history", params=params)
        return APIResponse[List[OfferWithHistory]](**response_data)
    
    def schedule_product_monitoring(
        self,
        identifier: str,
        frequency: Literal["hourly", "daily", "weekly"],
        retailer: Optional[str] = None
    ) -> APIResponse[Dict[str, Union[bool, str]]]:
        """
        Schedule product monitoring
        
        Args:
            identifier: Product identifier
            frequency: How often to refresh ('hourly', 'daily', 'weekly')
            retailer: Optional retailer to monitor
            
        Returns:
            Scheduling confirmation
            
        Example:
            >>> result = api.schedule_product_monitoring("012345678901", "daily")
            >>> print(f"Scheduled: {result.data['scheduled']}")
        """
        json_data = {
            "identifier": identifier,
            "frequency": frequency,
        }
        if retailer:
            json_data["retailer"] = retailer
        
        response_data = self._make_request("POST", "/products/schedule", json_data=json_data)
        return APIResponse[Dict[str, Union[bool, str]]](**response_data)
    
    def schedule_product_monitoring_batch(
        self,
        identifiers: List[str],
        frequency: Literal["hourly", "daily", "weekly"],
        retailer: Optional[str] = None
    ) -> APIResponse[List[Dict[str, Union[str, bool]]]]:
        """
        Schedule monitoring for multiple products
        
        Args:
            identifiers: List of product identifiers
            frequency: How often to refresh
            retailer: Optional retailer to monitor
            
        Returns:
            Scheduling confirmation for all products
        """
        json_data = {
            "identifiers": ",".join(identifiers),
            "frequency": frequency,
        }
        if retailer:
            json_data["retailer"] = retailer
        
        response_data = self._make_request("POST", "/products/schedule", json_data=json_data)
        return APIResponse[List[Dict[str, Union[str, bool]]]](**response_data)
    
    def get_scheduled_products(self) -> APIResponse[List[ScheduledProduct]]:
        """
        Get all scheduled products
        
        Returns:
            List of scheduled products
            
        Example:
            >>> scheduled = api.get_scheduled_products()
            >>> print(f"Monitoring {len(scheduled.data)} products")
        """
        response_data = self._make_request("GET", "/products/scheduled")
        return APIResponse[List[ScheduledProduct]](**response_data)
    
    def remove_product_from_schedule(
        self, identifier: str
    ) -> APIResponse[Dict[str, bool]]:
        """
        Remove product from monitoring schedule
        
        Args:
            identifier: Product identifier to remove
            
        Returns:
            Removal confirmation
            
        Example:
            >>> result = api.remove_product_from_schedule("012345678901")
            >>> print(f"Removed: {result.data['removed']}")
        """
        json_data = {"identifier": identifier}
        response_data = self._make_request("DELETE", "/products/schedule", json_data=json_data)
        return APIResponse[Dict[str, bool]](**response_data)
    
    def remove_products_from_schedule(
        self, identifiers: List[str]
    ) -> APIResponse[List[Dict[str, Union[str, bool]]]]:
        """
        Remove multiple products from monitoring schedule
        
        Args:
            identifiers: List of product identifiers to remove
            
        Returns:
            Removal confirmation for all products
        """
        json_data = {"identifiers": ",".join(identifiers)}
        response_data = self._make_request("DELETE", "/products/schedule", json_data=json_data)
        return APIResponse[List[Dict[str, Union[str, bool]]]](**response_data)
    
    def get_usage(self) -> APIResponse[UsageInfo]:
        """
        Get API usage information
        
        Returns:
            Current usage and credit information
            
        Example:
            >>> usage = api.get_usage()
            >>> print(f"Credits remaining: {usage.data.credits_remaining}")
        """
        response_data = self._make_request("GET", "/usage")
        return APIResponse[UsageInfo](**response_data)


def create_client(api_key: str, **kwargs) -> ShopSavvyDataAPI:
    """
    Create a new ShopSavvy Data API client
    
    Args:
        api_key: Your ShopSavvy API key
        **kwargs: Additional configuration options
        
    Returns:
        API client instance
        
    Example:
        >>> from shopsavvy import create_client
        >>> 
        >>> api = create_client("ss_live_your_api_key_here")
        >>> product = api.get_product_details("012345678901")
        >>> print(product.data.name)
    """
    config = ShopSavvyConfig(api_key=api_key, **kwargs)
    return ShopSavvyDataAPI(config)