"""GET /products/offers carries, per product, an ``in_store_prices`` list: shelf prices read
from shoppers' scanned receipts, labeled ``source: "user-collected"``."""

import json
from pathlib import Path

from shopsavvy import InStorePrice, ProductWithOffers

FIXTURE = json.loads((Path(__file__).parent / "fixture_offers_in_store.json").read_text())


def test_in_store_prices_parse(make_api):
    api, captured = make_api(200, FIXTURE)
    response = api.get_current_offers("011110838360")
    assert captured[0].url.path == "/v1/products/offers"
    product = response.data[0]
    assert isinstance(product, ProductWithOffers)
    in_store: InStorePrice = product.in_store_prices[0]
    assert in_store.source == "user-collected"
    assert in_store.retailer == "Kroger"
    assert in_store.store.address == "1014 Vine St, Cincinnati, OH 45202, USA"
    assert in_store.store.latitude == 39.1086
    assert in_store.price == 3.49
    assert in_store.observed_on == "2026-11-07"
    assert product.offers[0].retailer == "Walmart"


def test_in_store_prices_default_empty():
    body = json.loads(json.dumps(FIXTURE))
    del body["data"][0]["in_store_prices"]
    product = ProductWithOffers(**body["data"][0])
    assert product.in_store_prices == []
