"""POST bodies reach the wire as JSON with the field names the API reads
(refinery entrypoint-api.ts: productsBatch reads {identifiers, include};
webhooksCreate reads {url, events}; webhooksUpdate reads {url, events, is_active}).
1.1.0 passed body= to _make_request, which raised TypeError before any request."""

import json

import pytest
from pydantic import ValidationError

from shopsavvy import ShopSavvyConfig, __version__


def test_batch_lookup_sends_identifiers_and_include(make_api):
    api, captured = make_api(200, {"success": True, "data": []})

    api.batch_lookup(["611247373064", "B07G14HTBZ"], include=["offers", "reviews"])

    request = captured[0]
    assert request.method == "POST"
    assert request.url.path == "/v1/products/batch"
    assert json.loads(request.content) == {
        "identifiers": ["611247373064", "B07G14HTBZ"],
        "include": ["offers", "reviews"],
    }


def test_batch_lookup_omits_include_when_not_given(make_api):
    api, captured = make_api(200, {"success": True, "data": []})

    api.batch_lookup(["611247373064"])

    assert json.loads(captured[0].content) == {"identifiers": ["611247373064"]}


def test_create_webhook_sends_url_and_events(make_api):
    api, captured = make_api(200, {"success": True, "data": {"id": "wh_1"}})

    result = api.create_webhook("https://example.com/hook", ["price.drop"])

    request = captured[0]
    assert request.method == "POST"
    assert request.url.path == "/v1/webhooks"
    assert json.loads(request.content) == {
        "url": "https://example.com/hook",
        "events": ["price.drop"],
    }
    assert result == {"success": True, "data": {"id": "wh_1"}}


def test_update_webhook_sends_only_given_fields(make_api):
    api, captured = make_api(200, {"success": True})

    api.update_webhook("wh_1", is_active=False)

    request = captured[0]
    assert request.method == "PUT"
    assert request.url.path == "/v1/webhooks/wh_1"
    assert json.loads(request.content) == {"is_active": False}


def test_user_agent_carries_package_version(make_api):
    api, captured = make_api(200, {"success": True, "data": []})

    api.batch_lookup(["611247373064"])

    assert captured[0].headers["User-Agent"] == f"ShopSavvy-Python-SDK/{__version__}"
    assert captured[0].headers["Authorization"] == "Bearer ss_test_fixture_key"


def test_rejects_malformed_api_key():
    with pytest.raises(ValidationError):
        ShopSavvyConfig(api_key="not_a_key")
    assert ShopSavvyConfig(api_key="ss_live_abc").api_key == "ss_live_abc"
