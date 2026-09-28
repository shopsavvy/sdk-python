"""get_price_history against the exact wire shape of GET /v1/products/offers/history:
data is one entry PER PRODUCT, each with offers, each offer with its own history."""


from shopsavvy import (
    APIResponse,
    OfferWithHistory,
    PriceHistoryEntry,
    ProductWithPriceHistory,
)
from shopsavvy.models import PriceHistoryResponse

from .conftest import load_fixture


def test_sends_start_and_end_not_start_date_end_date(make_api):
    api, captured = make_api(200, load_fixture("fixture_price_history.json"))

    api.get_price_history("611247373064", "2022-11-20", "2022-11-27", retailer="amazon.com")

    assert len(captured) == 1
    request = captured[0]
    assert request.method == "GET"
    assert request.url.path == "/v1/products/offers/history"
    params = dict(request.url.params)
    assert params == {
        "ids": "611247373064",
        "start": "2022-11-20",
        "end": "2022-11-27",
        "retailer": "amazon.com",
    }
    assert "start_date" not in params and "end_date" not in params


def test_parses_products_offers_and_history(make_api):
    api, _ = make_api(200, load_fixture("fixture_price_history.json"))

    result = api.get_price_history("611247373064,611247369449", "2022-11-20", "2022-11-27")

    assert isinstance(result, APIResponse)
    assert result.success is True
    assert len(result.data) == 2

    kmini = result.data[0]
    assert isinstance(kmini, ProductWithPriceHistory)
    assert kmini.title == "Keurig K-Mini Single Serve Coffee Maker, Black"
    assert kmini.shopsavvy == "3ONn300xybP3y66ibqc1"
    assert kmini.barcode == "611247373064"
    assert kmini.amazon == "B07G14HTBZ"
    assert kmini.title_short == "Keurig K-Mini"
    assert kmini.rating == {"value": 4.6, "count": 51234}
    assert kmini.image_url.endswith("31jy5fSzyRL.jpg")
    assert len(kmini.offers) == 2

    amazon = kmini.offers[0]
    assert isinstance(amazon, OfferWithHistory)
    assert amazon.id == "0IUouCFtZEhxeOablTPl"
    assert amazon.retailer == "Amazon"
    assert amazon.price == 74.96
    assert amazon.currency == "USD"
    assert amazon.availability == "in"
    assert amazon.condition == "new"
    assert amazon.seller == "ACME Deals"
    assert amazon.url == "https://www.amazon.com/dp/B07G14HTBZ?m=A1GKQADQC2VI6E"
    assert amazon.timestamp == "2022-11-27T22:36:33.236Z"

    assert len(amazon.history) == 3
    assert all(isinstance(p, PriceHistoryEntry) for p in amazon.history)
    newest, middle, oldest = amazon.history
    assert (newest.timestamp, newest.price, newest.currency, newest.availability) == (
        "2022-11-27T22:36:33.236Z", 74.96, "USD", "in"
    )
    assert (middle.price, middle.availability) == (70.99, "out")
    # availability omitted and currency null on the wire -> None, never a guessed default
    assert oldest.price == 79.99
    assert oldest.availability is None
    assert oldest.currency is None

    bestbuy = kmini.offers[1]
    assert bestbuy.retailer == "Best Buy"
    assert bestbuy.availability is None  # key absent: availability unknown
    assert bestbuy.seller is None  # JSON null
    assert [p.price for p in bestbuy.history] == [59.99, 64.99]

    elite = result.data[1]
    assert elite.shopsavvy == "DrKWneG0MpFlZpwZXNYa"
    assert elite.category is None
    assert elite.amazon is None
    assert elite.images == []
    assert elite.image_url is None
    assert len(elite.offers) == 1
    assert elite.offers[0].retailer == "eBay"
    assert elite.offers[0].history == []  # eBay listings never carry history

    assert result.meta is not None
    assert result.meta.request_id == "req-7f3c9a"
    assert result.credits_used == 14
    assert result.credits_remaining == 986
    assert result.meta.rate_limit_remaining == 999


def test_exported_response_alias_matches_client_return_type(make_api):
    body = load_fixture("fixture_price_history.json")
    parsed = PriceHistoryResponse(**body)
    assert [p.shopsavvy for p in parsed.data] == ["3ONn300xybP3y66ibqc1", "DrKWneG0MpFlZpwZXNYa"]
    assert parsed.data[0].offers[0].history[0].price == 74.96


def test_offer_missing_history_key_defaults_to_empty_list(make_api):
    body = load_fixture("fixture_price_history.json")
    del body["data"][1]["offers"][0]["history"]
    api, _ = make_api(200, body)

    result = api.get_price_history("611247369449", "2022-11-20", "2022-11-27")

    assert result.data[1].offers[0].history == []


def test_product_without_offers_parses(make_api):
    body = load_fixture("fixture_price_history.json")
    body["data"][1]["offers"] = []
    api, _ = make_api(200, body)

    result = api.get_price_history("611247369449", "2022-11-20", "2022-11-27")

    assert result.data[1].offers == []
