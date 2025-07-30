# 🛍️ ShopSavvy Data API - Python SDK

[![PyPI version](https://badge.fury.io/py/shopsavvy-sdk.svg)](https://badge.fury.io/py/shopsavvy-sdk)
[![Python Support](https://img.shields.io/pypi/pyversions/shopsavvy-sdk.svg)](https://pypi.org/project/shopsavvy-sdk/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Downloads](https://pepy.tech/badge/shopsavvy-sdk)](https://pepy.tech/project/shopsavvy-sdk)

**The most comprehensive Python SDK for e-commerce product data and pricing intelligence.** 

Access real-time product information, pricing data, and historical trends across **thousands of retailers** and **millions of products** with the official [ShopSavvy Data API](https://shopsavvy.com/data).

---

## 🚀 Quick Start

### Installation

```bash
pip install shopsavvy-sdk
```

### Get Your API Key

1. 🌟 Visit [shopsavvy.com/data](https://shopsavvy.com/data)
2. 📝 Sign up for a free account
3. 💳 Choose a subscription plan
4. 🔑 Get your API key from the dashboard

### 30-Second Example

```python
from shopsavvy import create_client

# Initialize the client
api = create_client("ss_live_your_api_key_here")

# Look up any product by barcode, ASIN, or URL
product = api.get_product_details("012345678901")
print(f"📦 {product.data.name} by {product.data.brand}")

# Get current prices from all retailers
offers = api.get_current_offers("012345678901")
cheapest = min(offers.data, key=lambda x: x.price)
print(f"💰 Best price: ${cheapest.price} at {cheapest.retailer}")

# Set up price monitoring
api.schedule_product_monitoring("012345678901", "daily")
print("🔔 Price alerts activated!")
```

---

## 🎯 Key Features

| Feature | Description | Use Cases |
|---------|-------------|-----------|
| 🔍 **Universal Product Lookup** | Search by barcode, ASIN, URL, model number | Product catalogs, inventory management |
| 💲 **Real-Time Pricing** | Current prices across major retailers | Price comparison, competitive analysis |
| 📈 **Historical Data** | Price trends and availability over time | Market research, pricing strategy |
| 🔔 **Smart Monitoring** | Automated price tracking and alerts | Price drops, stock notifications |
| 🏪 **Multi-Retailer Support** | Amazon, Walmart, Target, Best Buy + more | Comprehensive market coverage |
| ⚡ **Batch Operations** | Process multiple products efficiently | Bulk analysis, data processing |
| 🛡️ **Type Safety** | Full Pydantic models with validation | Reliable data structures |
| 📊 **Multiple Formats** | JSON and CSV response options | Easy data integration |

---

## 🏗️ Installation & Setup

### Basic Installation
```bash
pip install shopsavvy-sdk
```

### Development Installation
```bash
git clone https://github.com/shopsavvy/sdk-python
cd sdk-python
pip install -e ".[dev]"
```

### Environment Setup
```bash
# Optional: Store your API key securely
export SHOPSAVVY_API_KEY="ss_live_your_api_key_here"
```

---

## 📖 Complete API Reference

### 🔧 Client Configuration

#### Method 1: Simple Client Creation (Recommended)
```python
from shopsavvy import create_client

# Basic setup
api = create_client("ss_live_your_api_key_here")

# With custom timeout and base URL
api = create_client(
    api_key="ss_live_your_api_key_here",
    timeout=60.0,
    base_url="https://api.shopsavvy.com/v1"
)
```

#### Method 2: Configuration Object
```python
from shopsavvy import ShopSavvyDataAPI, ShopSavvyConfig

config = ShopSavvyConfig(
    api_key="ss_live_your_api_key_here",
    timeout=45.0
)
api = ShopSavvyDataAPI(config)
```

#### Method 3: Context Manager (Auto-cleanup)
```python
# Automatically closes connections when done
with create_client("ss_live_your_api_key_here") as api:
    product = api.get_product_details("012345678901")
    print(product.data.name)
# Connection automatically closed here
```

### 🔍 Product Lookup

#### Single Product Lookup
```python
# Search by barcode (UPC/EAN)
product = api.get_product_details("012345678901")

# Search by Amazon ASIN
amazon_product = api.get_product_details("B08N5WRWNW")

# Search by product URL
url_product = api.get_product_details("https://www.amazon.com/dp/B08N5WRWNW")

# Search by model number
model_product = api.get_product_details("iPhone-14-Pro")

# Access product information
print(f"📦 Product: {product.data.name}")
print(f"🏷️ Brand: {product.data.brand}")
print(f"📂 Category: {product.data.category}")
print(f"🔢 Product ID: {product.data.product_id}")
print(f"📷 Image: {product.data.image_url}")
```

#### Batch Product Lookup
```python
# Look up multiple products at once
identifiers = [
    "012345678901",           # Barcode
    "B08N5WRWNW",            # Amazon ASIN
    "https://www.target.com/p/example",  # URL
    "MODEL-ABC123"            # Model number
]

products = api.get_product_details_batch(identifiers)

for product in products.data:
    print(f"✅ Found: {product.name} by {product.brand}")
    print(f"   ID: {product.product_id}")
    print(f"   Category: {product.category}")
    print("---")
```

#### CSV Format Support
```python
# Get product data in CSV format for easy processing
product_csv = api.get_product_details("012345678901", format="csv")

# Process with pandas
import pandas as pd
import io

df = pd.read_csv(io.StringIO(product_csv.data))
print(df.head())
```

### 💰 Current Pricing

#### Get All Current Offers
```python
# Get prices from all retailers
offers = api.get_current_offers("012345678901")

print(f"Found {len(offers.data)} offers:")
for offer in offers.data:
    print(f"🏪 {offer.retailer}: ${offer.price}")
    print(f"   📦 Condition: {offer.condition}")
    print(f"   ✅ Available: {offer.availability}")
    print(f"   🔗 Buy: {offer.url}")
    if offer.shipping:
        print(f"   🚚 Shipping: ${offer.shipping}")
    print("---")
```

#### Retailer-Specific Pricing
```python
# Get offers from specific retailers
amazon_offers = api.get_current_offers("012345678901", retailer="amazon")
walmart_offers = api.get_current_offers("012345678901", retailer="walmart")
target_offers = api.get_current_offers("012345678901", retailer="target")

print("Amazon prices:")
for offer in amazon_offers.data:
    print(f"  ${offer.price} - {offer.condition}")
```

#### Batch Pricing
```python
# Get current offers for multiple products
products = ["012345678901", "B08N5WRWNW", "045496596439"]
batch_offers = api.get_current_offers_batch(products)

for identifier, offers in batch_offers.data.items():
    best_price = min(offers, key=lambda x: x.price) if offers else None
    if best_price:
        print(f"{identifier}: Best price ${best_price.price} at {best_price.retailer}")
    else:
        print(f"{identifier}: No offers found")
```

### 📈 Price History & Trends

#### Basic Price History
```python
from datetime import datetime, timedelta

# Get 30 days of price history
end_date = datetime.now().strftime("%Y-%m-%d")
start_date = (datetime.now() - timedelta(days=30)).strftime("%Y-%m-%d")

history = api.get_price_history("012345678901", start_date, end_date)

for offer in history.data:
    print(f"🏪 {offer.retailer}:")
    print(f"   💰 Current price: ${offer.price}")
    print(f"   📊 Historical points: {len(offer.price_history)}")
    
    if offer.price_history:
        prices = [point.price for point in offer.price_history]
        print(f"   📉 Lowest: ${min(prices)}")
        print(f"   📈 Highest: ${max(prices)}")
        print(f"   📊 Average: ${sum(prices) / len(prices):.2f}")
    print("---")
```

#### Retailer-Specific History
```python
# Get price history from Amazon only
amazon_history = api.get_price_history(
    "012345678901", 
    "2024-01-01", 
    "2024-01-31",
    retailer="amazon"
)

for offer in amazon_history.data:
    print(f"Amazon price trends for {offer.retailer}:")
    for point in offer.price_history[-10:]:  # Last 10 data points
        print(f"  {point.date}: ${point.price} ({point.availability})")
```

### 🔔 Product Monitoring & Alerts

#### Schedule Single Product Monitoring
```python
# Monitor daily across all retailers
result = api.schedule_product_monitoring("012345678901", "daily")
if result.data.get("scheduled"):
    print("✅ Daily monitoring activated!")

# Monitor hourly at specific retailer
result = api.schedule_product_monitoring(
    "012345678901", 
    "hourly", 
    retailer="amazon"
)
print(f"Amazon monitoring: {result.data}")
```

#### Batch Monitoring Setup
```python
# Schedule multiple products for monitoring
products_to_monitor = [
    "012345678901",
    "B08N5WRWNW", 
    "045496596439"
]

batch_result = api.schedule_product_monitoring_batch(products_to_monitor, "daily")

for item in batch_result.data:
    if item.get('scheduled'):
        print(f"✅ Monitoring activated for {item['identifier']}")
    else:
        print(f"❌ Failed to monitor {item['identifier']}")
```

#### Manage Scheduled Products
```python
# View all monitored products
scheduled = api.get_scheduled_products()
print(f"📊 Currently monitoring {len(scheduled.data)} products:")

for product in scheduled.data:
    print(f"🔔 {product.identifier}")
    print(f"   📅 Frequency: {product.frequency}")
    print(f"   🏪 Retailer: {product.retailer or 'All retailers'}")
    print(f"   📅 Created: {product.created_at}")
    if product.last_refreshed:
        print(f"   🔄 Last refresh: {product.last_refreshed}")
    print("---")

# Remove products from monitoring
api.remove_product_from_schedule("012345678901")
print("🗑️  Removed from monitoring")

# Remove multiple products
api.remove_products_from_schedule(["012345678901", "B08N5WRWNW"])
print("🗑️  Batch removal complete")
```

### 📊 Usage & Analytics

```python
# Check your API usage
usage = api.get_usage()

print("📊 API Usage Summary:")
print(f"💳 Plan: {usage.data.plan_name}")
print(f"✅ Credits used: {usage.data.credits_used:,}")
print(f"🔋 Credits remaining: {usage.data.credits_remaining:,}")
print(f"📊 Total credits: {usage.data.credits_total:,}")
print(f"📅 Billing period: {usage.data.billing_period_start} to {usage.data.billing_period_end}")

# Calculate usage percentage
usage_percent = (usage.data.credits_used / usage.data.credits_total) * 100
print(f"📈 Usage: {usage_percent:.1f}%")
```

---

## 🛠️ Advanced Usage & Examples

### 🏆 Price Comparison Tool

```python
def find_best_deals(identifier: str, max_results: int = 5):
    """Find the best deals for a product across all retailers"""
    try:
        # Get product info
        product = api.get_product_details(identifier)
        print(f"🔍 Searching deals for: {product.data.name}")
        print(f"📦 Brand: {product.data.brand}")
        print("=" * 50)
        
        # Get all current offers
        offers = api.get_current_offers(identifier)
        
        if not offers.data:
            print("❌ No offers found")
            return
        
        # Filter and sort offers
        available_offers = [
            offer for offer in offers.data 
            if offer.availability == "in_stock"
        ]
        
        if not available_offers:
            print("❌ No in-stock offers found")
            return
            
        # Sort by total cost (price + shipping)
        def total_cost(offer):
            return offer.price + (offer.shipping or 0)
        
        sorted_offers = sorted(available_offers, key=total_cost)[:max_results]
        
        print(f"🏆 Top {len(sorted_offers)} Deals:")
        for i, offer in enumerate(sorted_offers, 1):
            total = total_cost(offer)
            print(f"{i}. 🏪 {offer.retailer}")
            print(f"   💰 Price: ${offer.price}")
            if offer.shipping:
                print(f"   🚚 Shipping: ${offer.shipping}")
            print(f"   💳 Total: ${total}")
            print(f"   📦 Condition: {offer.condition}")
            print(f"   🔗 Buy now: {offer.url}")
            print("---")
            
        # Calculate savings
        if len(sorted_offers) > 1:
            cheapest = total_cost(sorted_offers[0])
            most_expensive = total_cost(sorted_offers[-1])
            savings = most_expensive - cheapest
            print(f"💰 Potential savings: ${savings:.2f}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

# Usage
find_best_deals("012345678901")
```

### 🚨 Smart Price Alert System

```python
import time
from datetime import datetime

class PriceAlertBot:
    def __init__(self, api_client):
        self.api = api_client
        self.alerts = {}  # identifier -> target_price
    
    def add_alert(self, identifier: str, target_price: float):
        """Add a price alert for a product"""
        self.alerts[identifier] = target_price
        
        # Schedule monitoring
        self.api.schedule_product_monitoring(identifier, "daily")
        print(f"🔔 Alert set: {identifier} @ ${target_price}")
    
    def check_alerts(self):
        """Check all price alerts"""
        print(f"🔍 Checking {len(self.alerts)} price alerts...")
        
        for identifier, target_price in self.alerts.items():
            try:
                offers = self.api.get_current_offers(identifier)
                if not offers.data:
                    continue
                
                # Find best available offer
                best_offer = min(
                    [o for o in offers.data if o.availability == "in_stock"],
                    key=lambda x: x.price,
                    default=None
                )
                
                if best_offer and best_offer.price <= target_price:
                    self.trigger_alert(identifier, best_offer, target_price)
                    
            except Exception as e:
                print(f"❌ Error checking {identifier}: {e}")
    
    def trigger_alert(self, identifier: str, offer, target_price: float):
        """Trigger price alert notification"""
        product = self.api.get_product_details(identifier)
        
        print("🚨" * 10)
        print("💰 PRICE ALERT TRIGGERED!")
        print(f"📦 Product: {product.data.name}")
        print(f"🎯 Target: ${target_price}")
        print(f"💸 Current: ${offer.price} at {offer.retailer}")
        print(f"✅ Savings: ${target_price - offer.price:.2f}")
        print(f"🔗 Buy now: {offer.url}")
        print("🚨" * 10)
        
        # Remove alert after triggering
        del self.alerts[identifier]

# Usage
alert_bot = PriceAlertBot(api)
alert_bot.add_alert("012345678901", 199.99)
alert_bot.add_alert("B08N5WRWNW", 299.99)

# Run periodic checks
alert_bot.check_alerts()
```

### 📊 Market Analysis Dashboard

```python
import statistics
from collections import defaultdict

def analyze_market_trends(identifiers: list, days: int = 30):
    """Comprehensive market analysis for multiple products"""
    from datetime import datetime, timedelta
    
    end_date = datetime.now().strftime("%Y-%m-%d")
    start_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    print(f"📊 Market Analysis Report ({days} days)")
    print("=" * 50)
    
    for identifier in identifiers:
        try:
            # Get product info
            product = api.get_product_details(identifier)
            print(f"\\n📦 {product.data.name}")
            print(f"🏷️  {product.data.brand} | {product.data.category}")
            print("-" * 40)
            
            # Get price history
            history = api.get_price_history(identifier, start_date, end_date)
            
            retailer_stats = {}
            
            for offer in history.data:
                if not offer.price_history:
                    continue
                    
                prices = [point.price for point in offer.price_history]
                
                retailer_stats[offer.retailer] = {
                    'current_price': offer.price,
                    'avg_price': statistics.mean(prices),
                    'min_price': min(prices),
                    'max_price': max(prices),
                    'volatility': statistics.stdev(prices) if len(prices) > 1 else 0,
                    'data_points': len(prices),
                    'trend': calculate_trend(prices)
                }
            
            # Display results
            if retailer_stats:
                print("🏪 Retailer Analysis:")
                for retailer, stats in sorted(retailer_stats.items()):
                    print(f"  {retailer}:")
                    print(f"    💰 Current: ${stats['current_price']}")
                    print(f"    📊 Average: ${stats['avg_price']:.2f}")
                    print(f"    📉 Min: ${stats['min_price']} | 📈 Max: ${stats['max_price']}")
                    print(f"    📈 Trend: {stats['trend']}")
                    print(f"    📊 Data points: {stats['data_points']}")
                
                # Find best value
                best_retailer = min(retailer_stats.items(), key=lambda x: x[1]['current_price'])
                print(f"\\n🏆 Best Price: {best_retailer[0]} @ ${best_retailer[1]['current_price']}")
            else:
                print("❌ No price history available")
                
        except Exception as e:
            print(f"❌ Error analyzing {identifier}: {e}")

def calculate_trend(prices: list) -> str:
    """Calculate price trend direction"""
    if len(prices) < 2:
        return "Unknown"
    
    recent = prices[-7:]  # Last week
    older = prices[:-7]   # Everything else
    
    if not older:
        return "New"
    
    recent_avg = statistics.mean(recent)
    older_avg = statistics.mean(older)
    
    if recent_avg > older_avg * 1.05:  # 5% threshold
        return "📈 Rising"
    elif recent_avg < older_avg * 0.95:
        return "📉 Falling"
    else:
        return "➡️  Stable"

# Usage
products_to_analyze = [
    "012345678901",
    "B08N5WRWNW",
    "045496596439"
]

analyze_market_trends(products_to_analyze, days=60)
```

### 🔄 Bulk Product Management

```python
def bulk_product_manager(csv_file_path: str):
    """Manage products from CSV file"""
    import csv
    
    print("📂 Loading products from CSV...")
    
    products = []
    with open(csv_file_path, 'r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            products.append({
                'identifier': row['identifier'],
                'target_price': float(row.get('target_price', 0)),
                'monitor': row.get('monitor', 'true').lower() == 'true'
            })
    
    print(f"📊 Processing {len(products)} products...")
    
    # Batch lookup
    identifiers = [p['identifier'] for p in products]
    try:
        product_details = api.get_product_details_batch(identifiers)
        current_offers = api.get_current_offers_batch(identifiers)
        
        results = []
        
        for product, details in zip(products, product_details.data):
            offers = current_offers.data.get(product['identifier'], [])
            best_price = min([o.price for o in offers if o.availability == "in_stock"], default=None)
            
            result = {
                'identifier': product['identifier'],
                'name': details.name,
                'brand': details.brand,
                'target_price': product['target_price'],
                'current_best_price': best_price,
                'price_alert': best_price <= product['target_price'] if best_price else False,
                'offers_count': len(offers)
            }
            results.append(result)
            
            # Setup monitoring if requested
            if product['monitor']:
                api.schedule_product_monitoring(product['identifier'], "daily")
        
        # Generate report
        print("\\n📊 Bulk Analysis Report:")
        print("=" * 80)
        for result in results:
            status = "🚨 ALERT" if result['price_alert'] else "📊 TRACKING"
            print(f"{status} | {result['name']} by {result['brand']}")
            print(f"    🎯 Target: ${result['target_price']} | 💰 Current: ${result['current_best_price'] or 'N/A'}")
            print(f"    🏪 Offers: {result['offers_count']}")
            print()
            
    except Exception as e:
        print(f"❌ Error processing bulk products: {e}")

# Usage
# bulk_product_manager("my_products.csv")
```

### 🌐 Multi-Format Data Export

```python
def export_product_data(identifiers: list, format: str = "json"):
    """Export product data in various formats"""
    import json
    import csv
    from datetime import datetime
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    
    if format.lower() == "json":
        # Export as JSON
        products = api.get_product_details_batch(identifiers)
        offers = api.get_current_offers_batch(identifiers)
        
        export_data = {
            "exported_at": datetime.now().isoformat(),
            "products": []
        }
        
        for product in products.data:
            product_offers = offers.data.get(product.product_id, [])
            export_data["products"].append({
                "product": product.dict(),
                "offers": [offer.dict() for offer in product_offers]
            })
        
        filename = f"shopsavvy_export_{timestamp}.json"
        with open(filename, 'w') as f:
            json.dump(export_data, f, indent=2)
            
        print(f"✅ Exported {len(products.data)} products to {filename}")
        
    elif format.lower() == "csv":
        # Export as CSV
        filename = f"shopsavvy_export_{timestamp}.csv"
        
        with open(filename, 'w', newline='') as csvfile:
            fieldnames = ['product_id', 'name', 'brand', 'category', 'barcode', 
                         'retailer', 'price', 'availability', 'condition', 'url']
            writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
            writer.writeheader()
            
            for identifier in identifiers:
                try:
                    product = api.get_product_details(identifier)
                    offers = api.get_current_offers(identifier)
                    
                    for offer in offers.data:
                        writer.writerow({
                            'product_id': product.data.product_id,
                            'name': product.data.name,
                            'brand': product.data.brand,
                            'category': product.data.category,
                            'barcode': product.data.barcode,
                            'retailer': offer.retailer,
                            'price': offer.price,
                            'availability': offer.availability,
                            'condition': offer.condition,
                            'url': offer.url
                        })
                except Exception as e:
                    print(f"❌ Error exporting {identifier}: {e}")
        
        print(f"✅ Exported data to {filename}")

# Usage
export_product_data(["012345678901", "B08N5WRWNW"], format="json")
export_product_data(["012345678901", "B08N5WRWNW"], format="csv")
```

---

## 🔧 Error Handling & Best Practices

### Comprehensive Error Handling

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

def robust_product_lookup(identifier: str):
    """Example of robust error handling"""
    try:
        product = api.get_product_details(identifier)
        offers = api.get_current_offers(identifier)
        
        print(f"✅ Success: {product.data.name}")
        print(f"💰 Found {len(offers.data)} offers")
        
        return product, offers
        
    except AuthenticationError:
        print("❌ Authentication failed - check your API key")
        print("🔑 Get your key at: https://shopsavvy.com/data/dashboard")
        
    except NotFoundError:
        print(f"❌ Product not found: {identifier}")
        print("💡 Try a different identifier (barcode, ASIN, URL)")
        
    except RateLimitError:
        print("⏳ Rate limit exceeded - please slow down")
        print("💡 Consider upgrading your plan for higher limits")
        time.sleep(60)  # Wait before retrying
        
    except ValidationError as e:
        print(f"❌ Invalid request: {e}")
        print("💡 Check your parameters and try again")
        
    except TimeoutError:
        print("⏱️  Request timeout - API might be slow")
        print("💡 Try increasing timeout or retry later")
        
    except NetworkError as e:
        print(f"🌐 Network error: {e}")
        print("💡 Check your internet connection")
        
    except APIError as e:
        print(f"🚨 API Error: {e}")
        print("💡 This might be a temporary issue")
        
    return None, None

# Usage with retry logic
def lookup_with_retry(identifier: str, max_retries: int = 3):
    """Lookup with automatic retry on failures"""
    for attempt in range(max_retries):
        try:
            return api.get_product_details(identifier)
        except (TimeoutError, NetworkError) as e:
            if attempt < max_retries - 1:
                wait_time = 2 ** attempt  # Exponential backoff
                print(f"⏳ Retry {attempt + 1}/{max_retries} in {wait_time}s...")
                time.sleep(wait_time)
            else:
                raise e
```

### Rate Limiting Best Practices

```python
import time
from functools import wraps

def rate_limit(calls_per_second: float = 10):
    """Decorator to rate limit function calls"""
    min_interval = 1.0 / calls_per_second
    last_called = [0.0]
    
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            elapsed = time.time() - last_called[0]
            left_to_wait = min_interval - elapsed
            if left_to_wait > 0:
                time.sleep(left_to_wait)
            ret = func(*args, **kwargs)
            last_called[0] = time.time()
            return ret
        return wrapper
    return decorator

# Rate-limited API calls
@rate_limit(calls_per_second=5)  # Max 5 calls per second
def safe_get_offers(identifier: str):
    return api.get_current_offers(identifier)

# Batch processing with rate limiting
def process_products_safely(identifiers: list):
    """Process products with automatic rate limiting"""
    results = []
    total = len(identifiers)
    
    for i, identifier in enumerate(identifiers, 1):
        print(f"🔄 Processing {i}/{total}: {identifier}")
        try:
            offers = safe_get_offers(identifier)
            results.append((identifier, offers))
            print(f"   ✅ Found {len(offers.data)} offers")
        except Exception as e:
            print(f"   ❌ Error: {e}")
            results.append((identifier, None))
    
    return results
```

### Configuration Management

```python
import os
from dataclasses import dataclass

@dataclass
class ShopSavvySettings:
    """Application settings"""
    api_key: str
    timeout: float = 30.0
    max_retries: int = 3
    rate_limit: float = 10.0  # calls per second
    
    @classmethod
    def from_env(cls):
        """Load settings from environment variables"""
        api_key = os.getenv("SHOPSAVVY_API_KEY")
        if not api_key:
            raise ValueError("SHOPSAVVY_API_KEY environment variable required")
        
        return cls(
            api_key=api_key,
            timeout=float(os.getenv("SHOPSAVVY_TIMEOUT", "30.0")),
            max_retries=int(os.getenv("SHOPSAVVY_MAX_RETRIES", "3")),
            rate_limit=float(os.getenv("SHOPSAVVY_RATE_LIMIT", "10.0"))
        )

# Usage
settings = ShopSavvySettings.from_env()
api = create_client(settings.api_key, timeout=settings.timeout)
```

---

## 🧪 Testing & Development

### Running Tests

```bash
# Install development dependencies
pip install -e ".[dev]"

# Run all tests
pytest

# Run with coverage
pytest --cov=shopsavvy

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

### Example Test

```python
import pytest
from unittest.mock import Mock, patch
from shopsavvy import create_client, AuthenticationError

def test_client_creation():
    """Test client creation with valid API key"""
    api = create_client("ss_test_valid_key")
    assert api is not None

def test_invalid_api_key():
    """Test invalid API key handling"""
    with pytest.raises(ValueError):
        create_client("invalid_key_format")

@patch('shopsavvy.client.httpx.Client.request')
def test_product_lookup(mock_request):
    """Test product lookup with mocked response"""
    # Mock successful response
    mock_response = Mock()
    mock_response.status_code = 200
    mock_response.is_success = True
    mock_response.json.return_value = {
        "success": True,
        "data": {
            "product_id": "12345",
            "name": "Test Product",
            "brand": "Test Brand"
        }
    }
    mock_request.return_value = mock_response
    
    # Test the client
    api = create_client("ss_test_valid_key")
    product = api.get_product_details("012345678901")
    
    assert product.success is True
    assert product.data.name == "Test Product"
```

---

## 🚀 Production Deployment

### Docker Setup

```dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install -r requirements.txt

# Copy application
COPY . .

# Set environment variables
ENV SHOPSAVVY_API_KEY="your_api_key_here"
ENV SHOPSAVVY_TIMEOUT="30.0"

# Run application
CMD ["python", "app.py"]
```

### AWS Lambda Example

```python
import json
import os
from shopsavvy import create_client

# Initialize client outside handler for connection reuse
api = create_client(os.environ['SHOPSAVVY_API_KEY'])

def lambda_handler(event, context):
    """AWS Lambda handler for product lookup"""
    try:
        identifier = event.get('identifier')
        if not identifier:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'identifier required'})
            }
        
        # Get product data
        product = api.get_product_details(identifier)
        offers = api.get_current_offers(identifier)
        
        # Find best price
        best_offer = min(offers.data, key=lambda x: x.price) if offers.data else None
        
        response = {
            'product': {
                'name': product.data.name,
                'brand': product.data.brand,
                'category': product.data.category
            },
            'best_price': {
                'price': best_offer.price,
                'retailer': best_offer.retailer,
                'url': best_offer.url
            } if best_offer else None,
            'total_offers': len(offers.data)
        }
        
        return {
            'statusCode': 200,
            'body': json.dumps(response)
        }
        
    except Exception as e:
        return {
            'statusCode': 500,
            'body': json.dumps({'error': str(e)})
        }
```

### Environment Variables

```bash
# Required
export SHOPSAVVY_API_KEY="ss_live_your_api_key_here"

# Optional
export SHOPSAVVY_TIMEOUT="30.0"
export SHOPSAVVY_BASE_URL="https://api.shopsavvy.com/v1"
export SHOPSAVVY_MAX_RETRIES="3"
```

---

## 🌟 Real-World Use Cases

### 🛒 E-commerce Platform Integration

```python
class EcommerceIntegration:
    """Integration with e-commerce platforms"""
    
    def __init__(self, api_key: str):
        self.api = create_client(api_key)
    
    def enrich_product_catalog(self, product_skus: list):
        """Enrich existing product catalog with market data"""
        enriched_products = []
        
        for sku in product_skus:
            try:
                # Get competitive pricing
                offers = self.api.get_current_offers(sku)
                competitor_prices = [
                    offer.price for offer in offers.data 
                    if offer.retailer != "your-store"
                ]
                
                enrichment = {
                    'sku': sku,
                    'competitor_count': len(competitor_prices),
                    'min_competitor_price': min(competitor_prices) if competitor_prices else None,
                    'avg_competitor_price': sum(competitor_prices) / len(competitor_prices) if competitor_prices else None,
                    'price_position': self.calculate_price_position(sku, competitor_prices)
                }
                
                enriched_products.append(enrichment)
                
            except Exception as e:
                print(f"❌ Error enriching {sku}: {e}")
        
        return enriched_products
    
    def calculate_price_position(self, sku: str, competitor_prices: list) -> str:
        """Calculate where your price stands vs competitors"""
        if not competitor_prices:
            return "no_competition"
        
        your_price = self.get_your_price(sku)  # Your implementation
        if not your_price:
            return "unknown"
        
        cheaper_count = sum(1 for price in competitor_prices if price < your_price)
        total_competitors = len(competitor_prices)
        
        if cheaper_count == 0:
            return "most_expensive"
        elif cheaper_count == total_competitors:
            return "cheapest"
        elif cheaper_count < total_competitors / 3:
            return "premium"
        elif cheaper_count > total_competitors * 2/3:
            return "budget"
        else:
            return "competitive"
```

### 🏢 Business Intelligence Dashboard

```python
class BusinessIntelligenceDashboard:
    """BI dashboard for retail insights"""
    
    def __init__(self, api_key: str):
        self.api = create_client(api_key)
    
    def generate_market_report(self, category: str, time_period: int = 30):
        """Generate comprehensive market report"""
        from datetime import datetime, timedelta
        
        # Get category products (you'd have your own product database)
        category_products = self.get_category_products(category)
        
        report = {
            'category': category,
            'analysis_date': datetime.now().isoformat(),
            'time_period_days': time_period,
            'products_analyzed': len(category_products),
            'insights': {}
        }
        
        # Analyze each product
        price_trends = []
        retailer_coverage = defaultdict(int)
        availability_stats = defaultdict(int)
        
        for product_id in category_products:
            try:
                # Get current market state
                offers = self.api.get_current_offers(product_id)
                
                for offer in offers.data:
                    retailer_coverage[offer.retailer] += 1
                    availability_stats[offer.availability] += 1
                
                # Get price trends
                start_date = (datetime.now() - timedelta(days=time_period)).strftime("%Y-%m-%d")
                end_date = datetime.now().strftime("%Y-%m-%d")
                
                history = self.api.get_price_history(product_id, start_date, end_date)
                
                for offer_history in history.data:
                    if offer_history.price_history:
                        prices = [p.price for p in offer_history.price_history]
                        trend = self.calculate_trend_percentage(prices)
                        price_trends.append(trend)
                        
            except Exception as e:
                print(f"❌ Error analyzing {product_id}: {e}")
        
        # Compile insights
        report['insights'] = {
            'avg_price_trend': sum(price_trends) / len(price_trends) if price_trends else 0,
            'top_retailers': dict(sorted(retailer_coverage.items(), key=lambda x: x[1], reverse=True)[:10]),
            'availability_breakdown': dict(availability_stats),
            'market_volatility': statistics.stdev(price_trends) if len(price_trends) > 1 else 0
        }
        
        return report
```

### 📱 Mobile App Backend

```python
from flask import Flask, jsonify, request
from shopsavvy import create_client

app = Flask(__name__)
api = create_client(os.environ['SHOPSAVVY_API_KEY'])

@app.route('/api/product/scan', methods=['POST'])
def scan_product():
    """Handle barcode scans from mobile app"""
    data = request.get_json()
    barcode = data.get('barcode')
    
    if not barcode:
        return jsonify({'error': 'Barcode required'}), 400
    
    try:
        # Get product details
        product = api.get_product_details(barcode)
        
        # Get current offers
        offers = api.get_current_offers(barcode)
        
        # Find best deals
        available_offers = [o for o in offers.data if o.availability == "in_stock"]
        best_offer = min(available_offers, key=lambda x: x.price) if available_offers else None
        
        response = {
            'product': {
                'name': product.data.name,
                'brand': product.data.brand,
                'image_url': product.data.image_url,
                'category': product.data.category
            },
            'pricing': {
                'best_price': best_offer.price if best_offer else None,
                'best_retailer': best_offer.retailer if best_offer else None,
                'buy_url': best_offer.url if best_offer else None,
                'total_offers': len(available_offers),
                'all_offers': [
                    {
                        'retailer': offer.retailer,
                        'price': offer.price,
                        'availability': offer.availability,
                        'condition': offer.condition,
                        'url': offer.url
                    }
                    for offer in available_offers[:5]  # Top 5 offers
                ]
            }
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

@app.route('/api/product/alerts', methods=['POST'])
def create_price_alert():
    """Create price alert for mobile users"""
    data = request.get_json()
    product_id = data.get('product_id')
    target_price = data.get('target_price')
    user_id = data.get('user_id')  # Your user system
    
    try:
        # Schedule monitoring
        result = api.schedule_product_monitoring(product_id, "daily")
        
        # Store alert in your database
        # store_price_alert(user_id, product_id, target_price)
        
        return jsonify({
            'success': True,
            'message': 'Price alert created successfully',
            'monitoring_active': result.data.get('scheduled', False)
        })
        
    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
```

---

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Quick Contribution Guide

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes** with tests
4. **Run the test suite**: `pytest`
5. **Submit a pull request**

---

## 📚 Additional Resources

| Resource | Link | Description |
|----------|------|-------------|
| 🌐 **API Documentation** | [shopsavvy.com/data/documentation](https://shopsavvy.com/data/documentation) | Complete API reference |
| 📊 **Dashboard** | [shopsavvy.com/data/dashboard](https://shopsavvy.com/data/dashboard) | Manage your API keys and usage |
| 💬 **Support** | [business@shopsavvy.com](mailto:business@shopsavvy.com) | Get help from our team |
| 🐛 **Issues** | [GitHub Issues](https://github.com/shopsavvy/sdk-python/issues) | Report bugs and request features |
| 📦 **PyPI** | [pypi.org/project/shopsavvy-sdk](https://pypi.org/project/shopsavvy-sdk/) | Python package repository |
| 📖 **Changelog** | [GitHub Releases](https://github.com/shopsavvy/sdk-python/releases) | Version history and updates |

---

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

## 🏢 About ShopSavvy

**ShopSavvy** has been helping shoppers save money since 2008. With over **40 million downloads** and **millions of active users**, we're the most trusted name in price comparison and shopping intelligence.

Our **Data API** provides the same powerful product data and pricing intelligence that powers our consumer app, now available to developers and businesses worldwide.

### Why Choose ShopSavvy?

- ✅ **13+ Years** of e-commerce data expertise
- ✅ **Millions of Products** across thousands of retailers
- ✅ **Real-Time Data** updated continuously
- ✅ **Enterprise Scale** trusted by major brands
- ✅ **Developer Friendly** with comprehensive tools and support

---

**🚀 Ready to get started?** [Get your API key](https://shopsavvy.com/data) and start building amazing e-commerce applications today!

**💬 Need help?** Contact us at [business@shopsavvy.com](mailto:business@shopsavvy.com) or visit [shopsavvy.com/data](https://shopsavvy.com/data) for more information.

---

<div align="center">

**Made with ❤️ by the ShopSavvy Team**

[Website](https://shopsavvy.com) • [API Docs](https://shopsavvy.com/data/documentation) • [Dashboard](https://shopsavvy.com/data/dashboard) • [Support](mailto:business@shopsavvy.com)

</div>