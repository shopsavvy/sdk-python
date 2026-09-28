"""Scheduling endpoints read ONLY query parameters (refinery entrypoint-api.ts
`schedule` / `unschedule`): PUT|DELETE /v1/products/scheduled?ids=...[&schedule=][&retailer=].
Any JSON body is ignored by the server, so these tests assert no body is sent."""

from shopsavvy import MessageResponse, ScheduledProduct

SCHEDULED_BODY = {
    "success": True,
    "data": [
        {
            "title": "Keurig K-Mini Single Serve Coffee Maker, Black",
            "shopsavvy": "3ONn300xybP3y66ibqc1",
            "barcode": "611247373064",
            "brand": "Keurig",
            "category": None,
            "images": [],
            "schedule": "daily",
            "retailer": "amazon.com",
        },
        {
            "title": "Keurig K-Elite Single Serve K-Cup Pod Maker",
            "shopsavvy": "DrKWneG0MpFlZpwZXNYa",
            "barcode": "611247369449",
            "images": [],
            "schedule": "daily",
        },
    ],
    "meta": {"request_id": "req-1", "credits_used": 2, "credits_remaining": 998, "rate_limit_remaining": 999},
}

UNSCHEDULE_BODY = {
    "success": True,
    "message": "Products successfully removed from schedule",
    "meta": {"request_id": "req-2", "credits_used": 0, "credits_remaining": 0, "rate_limit_remaining": 0},
}


def _assert_query_only(request, method, params):
    assert request.method == method
    assert request.url.path == "/v1/products/scheduled"
    assert dict(request.url.params) == params
    assert request.content == b""


def test_schedule_single_sends_query_params(make_api):
    api, captured = make_api(200, SCHEDULED_BODY)

    result = api.schedule_product_monitoring("611247373064", "daily")

    _assert_query_only(captured[0], "PUT", {"ids": "611247373064", "schedule": "daily"})
    assert all(isinstance(p, ScheduledProduct) for p in result.data)
    assert result.data[0].schedule == "daily"
    assert result.data[0].frequency == "daily"
    assert result.data[0].retailer == "amazon.com"
    assert result.data[1].retailer is None
    assert result.credits_used == 2


def test_schedule_single_with_retailer(make_api):
    api, captured = make_api(200, SCHEDULED_BODY)

    api.schedule_product_monitoring("611247373064", "hourly", retailer="amazon.com")

    _assert_query_only(
        captured[0], "PUT", {"ids": "611247373064", "schedule": "hourly", "retailer": "amazon.com"}
    )


def test_schedule_batch_joins_ids_with_commas(make_api):
    api, captured = make_api(200, SCHEDULED_BODY)

    result = api.schedule_product_monitoring_batch(["611247373064", "B07G14HTBZ"], "weekly")

    _assert_query_only(
        captured[0], "PUT", {"ids": "611247373064,B07G14HTBZ", "schedule": "weekly"}
    )
    # the comma survives URL encoding and nothing else is mangled
    assert captured[0].url.query in (
        b"ids=611247373064%2CB07G14HTBZ&schedule=weekly",
        b"ids=611247373064,B07G14HTBZ&schedule=weekly",
    )
    assert [p.shopsavvy for p in result.data] == ["3ONn300xybP3y66ibqc1", "DrKWneG0MpFlZpwZXNYa"]


def test_schedule_batch_with_retailer(make_api):
    api, captured = make_api(200, SCHEDULED_BODY)

    api.schedule_product_monitoring_batch(["611247373064", "611247369449"], "daily", retailer="bestbuy.com")

    _assert_query_only(
        captured[0],
        "PUT",
        {"ids": "611247373064,611247369449", "schedule": "daily", "retailer": "bestbuy.com"},
    )


def test_identifier_with_reserved_characters_is_url_encoded(make_api):
    api, captured = make_api(200, SCHEDULED_BODY)

    api.schedule_product_monitoring("https://www.amazon.com/dp/B07G14HTBZ?th=1&psc=1", "daily")

    assert dict(captured[0].url.params)["ids"] == "https://www.amazon.com/dp/B07G14HTBZ?th=1&psc=1"
    assert b"psc=1&" not in captured[0].url.query  # the & inside the id is escaped


def test_unschedule_single_sends_ids_query(make_api):
    api, captured = make_api(200, UNSCHEDULE_BODY)

    result = api.remove_product_from_schedule("611247373064")

    _assert_query_only(captured[0], "DELETE", {"ids": "611247373064"})
    assert isinstance(result, MessageResponse)
    assert result.success is True
    assert result.message == "Products successfully removed from schedule"
    assert result.meta.request_id == "req-2"


def test_unschedule_batch_joins_ids(make_api):
    api, captured = make_api(200, UNSCHEDULE_BODY)

    api.remove_products_from_schedule(["611247373064", "611247369449"])

    _assert_query_only(captured[0], "DELETE", {"ids": "611247373064,611247369449"})


def test_get_scheduled_products_parses_wire_shape(make_api):
    body = dict(SCHEDULED_BODY)
    body["data"] = SCHEDULED_BODY["data"] + [
        {"title": "Business 4h schedule", "shopsavvy": "x1", "images": []}
    ]
    api, captured = make_api(200, body)

    result = api.get_scheduled_products()

    assert captured[0].method == "GET"
    assert captured[0].url.path == "/v1/products/scheduled"
    assert len(result.data) == 3
    assert result.data[0].title.startswith("Keurig K-Mini")
    assert result.data[0].barcode == "611247373064"
    assert result.data[2].schedule is None  # interval with no Data API label is omitted
