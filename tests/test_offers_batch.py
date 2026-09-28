"""GET /products/offers returns one entry PER PRODUCT (publicProductForProduct fields)
with an ``offers`` list (refinery entrypoint-api.ts `offers` handler). The batch method
used to type ``data`` as ``Dict[str, List[Offer]]`` keyed by identifier — a shape the API
has never sent — so every real 200 raised a ValidationError."""

from shopsavvy import ProductWithOffers

OFFERS_BATCH_BODY = {
    "success": True,
    "data": [
        {
            "title": "Keurig K-Mini Single Serve Coffee Maker, Black",
            "shopsavvy": "3ONn300xybP3y66ibqc1",
            "barcode": "611247373064",
            "amazon": "B07GV2S1GS",
            "brand": "Keurig",
            "category": None,
            "color": None,
            "model": None,
            "mpn": None,
            "images": ["https://images.example/k-mini.jpg"],
            "offers": [
                {
                    "id": "o-amazon-1",
                    "availability": "in",
                    "condition": "new",
                    "retailer": "Amazon",
                    "currency": "USD",
                    "price": 79.99,
                    "URL": "https://www.amazon.com/dp/B07GV2S1GS",
                    "timestamp": "2026-09-20T10:00:00.000Z",
                    "history": [],
                },
                {
                    "id": "o-target-1",
                    "condition": "new",
                    "retailer": "Target",
                    "currency": "USD",
                    "price": 89.99,
                    "seller": "Target",
                    "URL": "https://www.target.com/p/-/A-1",
                    "timestamp": "2026-09-19T10:00:00.000Z",
                    "history": [],
                },
            ],
        },
        {
            "title": "Keurig K-Elite Single Serve K-Cup Pod Maker",
            "shopsavvy": "DrKWneG0MpFlZpwZXNYa",
            "barcode": "611247369449",
            "images": [],
            "offers": [],
        },
    ],
    "meta": {"request_id": "req-o", "credits_used": 3, "credits_remaining": 997, "rate_limit_remaining": 999},
}


def test_offers_batch_parses_products_with_offers(make_api):
    api, captured = make_api(200, OFFERS_BATCH_BODY)

    result = api.get_current_offers_batch(["611247373064", "611247369449"], retailer="amazon.com")

    assert captured[0].method == "GET"
    assert captured[0].url.path == "/v1/products/offers"
    assert dict(captured[0].url.params) == {"ids": "611247373064,611247369449", "retailer": "amazon.com"}
    assert isinstance(result.data, list)
    assert all(isinstance(p, ProductWithOffers) for p in result.data)
    first, second = result.data
    assert first.barcode == "611247373064"
    assert first.amazon == "B07GV2S1GS"
    assert [o.retailer for o in first.offers] == ["Amazon", "Target"]
    assert first.offers[0].price == 79.99
    assert first.offers[0].availability == "in"
    assert first.offers[1].availability is None  # "unknown" is omitted by the API
    assert first.offers[1].seller == "Target"
    assert second.offers == []
    assert result.credits_used == 3
