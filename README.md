# ShopSavvy Data API - Python SDK

[![PyPI version](https://badge.fury.io/py/shopsavvy-sdk.svg)](https://badge.fury.io/py/shopsavvy-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/shopsavvy-sdk.svg)](https://pypi.org/project/shopsavvy-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

Official Python SDK for the [ShopSavvy Data API](https://shopsavvy.com/data). Access product data, pricing information, and price history across thousands of retailers and millions of products.

## 🚀 Quick Start

### Installation

```bash
pip install shopsavvy-sdk
```

### Get Your API Key

1. Visit [shopsavvy.com/data](https://shopsavvy.com/data)
2. Sign up for an account
3. Choose a subscription plan
4. Get your API key from the dashboard

### Basic Usage

```python
from shopsavvy import create_client

# Initialize the client
api = create_client("ss_live_your_api_key_here")

# Look up a product by barcode
product = api.get_product_details("012345678901")
print(product.data.name)

# Get current prices from all retailers
offers = api.get_current_offers("012345678901")
for offer in offers.data:
    print(f"{offer.retailer}: ${offer.price}")

# Get price history
history = api.get_price_history(
    "012345678901",
    "2024-01-01", 
    "2024-01-31"
)
```

## 📖 API Reference

### Client Configuration

```python
from shopsavvy import ShopSavvyDataAPI, ShopSavvyConfig

# Method 1: Using create_client (recommended)
api = create_client(
    api_key="ss_live_your_api_key_here",
    timeout=30.0,  # optional
    base_url="https://api.shopsavvy.com/v1"  # optional
)

# Method 2: Using configuration object
config = ShopSavvyConfig(
    api_key="ss_live_your_api_key_here",
    timeout=30.0
)
api = ShopSavvyDataAPI(config)

# Method 3: Using context manager (auto-closes connection)
with create_client("ss_live_your_api_key_here") as api:
    product = api.get_product_details("012345678901")
```

### Product Lookup

#### Single Product
```python
# Look up by barcode, ASIN, URL, or model number
product = api.get_product_details("012345678901")
amazon_product = api.get_product_details("B08N5WRWNW")  
url_product = api.get_product_details("https://www.amazon.com/dp/B08N5WRWNW")

print(f"Product: {product.data.name}")
print(f"Brand: {product.data.brand}")
print(f"Category: {product.data.category}")
```

#### Multiple Products
```python
products = api.get_product_details_batch([
    "012345678901",
    "B08N5WRWNW",
    "https://www.bestbuy.com/site/product/123456"
])

for product in products.data:
    print(f"{product.name} by {product.brand}")
```

### Current Pricing

#### All Retailers
```python
offers = api.get_current_offers("012345678901")
print(f"Found {len(offers.data)} offers")

# Sort by price
sorted_offers = sorted(offers.data, key=lambda x: x.price)
cheapest = sorted_offers[0]
print(f"Best price: {cheapest.retailer} - ${cheapest.price}")
```

#### Specific Retailer
```python
amazon_offers = api.get_current_offers("012345678901", retailer="amazon")
target_offers = api.get_current_offers("012345678901", retailer="target")
```

#### Multiple Products
```python
batch_offers = api.get_current_offers_batch([
    "012345678901",
    "B08N5WRWNW"
])

for identifier, offers in batch_offers.data.items():
    print(f"{identifier}: {len(offers)} offers")
```

### Price History

```python
# Get 30 days of price history
history = api.get_price_history(
    "012345678901",
    "2024-01-01",
    "2024-01-31"
)

for offer in history.data:
    print(f"{offer.retailer}:")
    print(f"  Current price: ${offer.price}")
    print(f"  Historical data points: {len(offer.price_history)}")
    
    # Analyze price trend
    prices = [point.price for point in offer.price_history]
    avg_price = sum(prices) / len(prices)
    min_price = min(prices)
    max_price = max(prices)
    
    print(f"  Average: ${avg_price:.2f}")
    print(f"  Range: ${min_price} - ${max_price}")

# Get retailer-specific price history
amazon_history = api.get_price_history(
    "012345678901",
    "2024-01-01",
    "2024-01-31",
    retailer="amazon"
)
```

### Product Monitoring

#### Schedule Monitoring
```python
# Monitor daily across all retailers
result = api.schedule_product_monitoring("012345678901", "daily")
print(f"Scheduled: {result.data['scheduled']}")

# Monitor hourly at Amazon only
api.schedule_product_monitoring(
    "012345678901", 
    "hourly", 
    retailer="amazon"
)

# Schedule multiple products
batch_result = api.schedule_product_monitoring_batch([
    "012345678901",
    "B08N5WRWNW"
], "daily")
```

#### Manage Scheduled Products
```python
# Get all scheduled products
scheduled = api.get_scheduled_products()
print(f"Monitoring {len(scheduled.data)} products")

for product in scheduled.data:
    print(f"{product.identifier}: {product.frequency} at {product.retailer or 'all retailers'}")

# Remove from schedule
api.remove_product_from_schedule("012345678901")

# Remove multiple products
api.remove_products_from_schedule(["012345678901", "B08N5WRWNW"])
```

### Usage Tracking

```python
usage = api.get_usage()
print(f"Credits remaining: {usage.data.credits_remaining}")
print(f"Credits used: {usage.data.credits_used}")
print(f"Plan: {usage.data.plan_name}")
print(f"Billing period: {usage.data.billing_period_start} to {usage.data.billing_period_end}")
```

## 🔧 Advanced Usage

### Error Handling

```python
from shopsavvy import (
    APIError, 
    AuthenticationError, 
    RateLimitError, 
    NotFoundError,
    ValidationError,
    TimeoutError,
    NetworkError
)

try:
    product = api.get_product_details("invalid-identifier")
except NotFoundError:
    print("Product not found")
except AuthenticationError:
    print("Invalid API key")
except RateLimitError:
    print("Rate limit exceeded - slow down requests")
except ValidationError as e:
    print(f"Invalid request parameters: {e}")
except TimeoutError:
    print("Request timed out")
except NetworkError as e:
    print(f"Network error: {e}")
except APIError as e:
    print(f"API error: {e}")
```

### Response Format

All API methods return a consistent response format:

```python
from shopsavvy.models import APIResponse

response = api.get_product_details("012345678901")

print(f"Success: {response.success}")
print(f"Data: {response.data}")
print(f"Credits used: {response.credits_used}")
print(f"Credits remaining: {response.credits_remaining}")

# Access the actual data
product = response.data
print(f"Product name: {product.name}")
```

### CSV Format

Some endpoints support CSV format for easier data processing:

```python
# Get product details in CSV format
product_csv = api.get_product_details("012345678901", format="csv")

# Get offers in CSV format
offers_csv = api.get_current_offers("012345678901", format="csv")

# Process with pandas
import pandas as pd
import io

df = pd.read_csv(io.StringIO(offers_csv.data))
print(df.head())
```

### Type Safety

The SDK is built with full type annotations and Pydantic models:

```python
from shopsavvy.models import ProductDetails, Offer, UsageInfo

# Type hints work perfectly
def analyze_product(product: ProductDetails) -> None:
    print(f"Analyzing {product.name}")
    # IDE will provide autocompletion for all fields

def find_best_offer(offers: list[Offer]) -> Offer:
    return min(offers, key=lambda x: x.price)

# Runtime validation
try:
    product = ProductDetails(
        product_id="123",
        name="Test Product"
        # All required fields validated automatically
    )
except ValidationError as e:
    print(f"Invalid product data: {e}")
```

## 💡 Examples

### Price Comparison Tool
```python
def compare_prices(identifier: str):
    """Compare prices across all retailers"""
    offers = api.get_current_offers(identifier)
    
    if not offers.data:
        print("No offers found")
        return
    
    sorted_offers = sorted(offers.data, key=lambda x: x.price)
    cheapest = sorted_offers[0]
    most_expensive = sorted_offers[-1]
    
    print(f"🏆 Best price: {cheapest.retailer} - ${cheapest.price}")
    print(f"💸 Highest price: {most_expensive.retailer} - ${most_expensive.price}")
    print(f"💰 Potential savings: ${most_expensive.price - cheapest.price}")
    
    return {
        'best_offer': cheapest,
        'worst_offer': most_expensive,
        'savings': most_expensive.price - cheapest.price
    }

# Usage
comparison = compare_prices("012345678901")
```

### Price Alert System
```python
def setup_price_alert(identifier: str, target_price: float):
    """Set up price monitoring and alert"""
    # Schedule daily monitoring
    api.schedule_product_monitoring(identifier, "daily")
    
    # Check current prices
    offers = api.get_current_offers(identifier)
    best_offer = min(offers.data, key=lambda x: x.price)
    
    if best_offer.price <= target_price:
        print(f"🎉 Target price reached!")
        print(f"💸 {best_offer.retailer}: ${best_offer.price}")
        print(f"🔗 Buy now: {best_offer.url}")
        return True
    else:
        print(f"⏰ Monitoring {identifier}")
        print(f"💰 Current best: ${best_offer.price} (target: ${target_price})")
        print(f"📈 Need ${best_offer.price - target_price:.2f} price drop")
        return False

# Usage
setup_price_alert("012345678901", 299.99)
```

### Historical Price Analysis
```python
from datetime import datetime, timedelta
import statistics

def analyze_price_trends(identifier: str, days: int = 30):
    """Analyze price trends over specified period"""
    end_date = datetime.now()
    start_date = end_date - timedelta(days=days)
    
    history = api.get_price_history(
        identifier,
        start_date.strftime("%Y-%m-%d"),
        end_date.strftime("%Y-%m-%d")
    )
    
    analysis = {}
    
    for offer in history.data:
        prices = [point.price for point in offer.price_history]
        
        if not prices:
            continue
            
        analysis[offer.retailer] = {
            'current_price': offer.price,
            'average_price': statistics.mean(prices),
            'median_price': statistics.median(prices),
            'min_price': min(prices),
            'max_price': max(prices),
            'price_volatility': statistics.stdev(prices) if len(prices) > 1 else 0,
            'data_points': len(prices)
        }
        
        # Price trend analysis
        if len(prices) >= 2:
            recent_avg = statistics.mean(prices[-7:])  # Last week
            older_avg = statistics.mean(prices[:-7])   # Everything else
            trend = "📈 Rising" if recent_avg > older_avg else "📉 Falling"
            analysis[offer.retailer]['trend'] = trend
    
    return analysis

# Usage
trends = analyze_price_trends("012345678901", days=60)
for retailer, data in trends.items():
    print(f"{retailer}:")
    print(f"  Current: ${data['current_price']}")
    print(f"  Average: ${data['average_price']:.2f}")
    print(f"  Range: ${data['min_price']} - ${data['max_price']}")
    print(f"  Trend: {data.get('trend', 'Unknown')}")
```

### Bulk Product Monitoring
```python
def setup_bulk_monitoring(identifiers: list[str], frequency: str = "daily"):
    """Set up monitoring for multiple products"""
    # Schedule all products
    result = api.schedule_product_monitoring_batch(identifiers, frequency)
    
    successful = []
    failed = []
    
    for item in result.data:
        if item['scheduled']:
            successful.append(item['identifier'])
        else:
            failed.append(item['identifier'])
    
    print(f"✅ Successfully scheduled: {len(successful)} products")
    print(f"❌ Failed to schedule: {len(failed)} products")
    
    if failed:
        print("Failed products:")
        for identifier in failed:
            print(f"  - {identifier}")
    
    return {'successful': successful, 'failed': failed}

# Usage
products_to_monitor = [
    "012345678901",
    "B08N5WRWNW", 
    "045496596439"
]
setup_bulk_monitoring(products_to_monitor, "daily")
```

## 🛠️ Development

### Installing for Development

```bash
git clone https://github.com/shopsavvy/python-sdk
cd python-sdk
pip install -e ".[dev]"
```

### Running Tests

```bash
# Run all tests
pytest

# Run with coverage
pytest --cov=src/shopsavvy

# Run specific test file
pytest tests/test_client.py

# Run with verbose output
pytest -v
```

### Code Quality

```bash
# Format code
black src tests

# Sort imports
isort src tests

# Type checking
mypy src

# Linting
flake8 src tests
```

### Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on contributing to this project.

## 📚 Additional Resources

- [ShopSavvy Data API Documentation](https://shopsavvy.com/data/documentation)
- [API Dashboard](https://shopsavvy.com/data/dashboard)
- [Support](mailto:business@shopsavvy.com)

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🏢 About ShopSavvy

ShopSavvy is a price comparison and shopping app that helps users find the best deals on products across various retailers. Since 2008, ShopSavvy has been downloaded over 40 million times and helps millions of users save money every day.

Our Data API provides the same powerful product data and pricing intelligence that powers our consumer app, available to developers and businesses worldwide.

---

**Need help?** Contact us at [business@shopsavvy.com](mailto:business@shopsavvy.com) or visit [shopsavvy.com/data](https://shopsavvy.com/data) for more information.