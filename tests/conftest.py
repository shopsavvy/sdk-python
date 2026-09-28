"""Shared helpers: drive the real ShopSavvyDataAPI through an httpx.MockTransport so
every test exercises the SDK's own request building and response parsing — only the
network hop is replaced."""

import json
from pathlib import Path
from typing import Callable, List

import httpx
import pytest

from shopsavvy import ShopSavvyConfig, ShopSavvyDataAPI

FIXTURES = Path(__file__).parent


def load_fixture(name: str) -> dict:
    return json.loads((FIXTURES / name).read_text())


@pytest.fixture
def make_api() -> Callable:
    """Returns (api, captured_requests) for a handler returning (status, json_body)."""

    clients: List[ShopSavvyDataAPI] = []

    def _make(status: int, body: dict):
        captured: List[httpx.Request] = []

        def handler(request: httpx.Request) -> httpx.Response:
            captured.append(request)
            return httpx.Response(status, json=body)

        api = ShopSavvyDataAPI(
            ShopSavvyConfig(api_key="ss_test_fixture_key"),
            transport=httpx.MockTransport(handler),
        )
        clients.append(api)
        return api, captured

    yield _make
    for api in clients:
        api.close()
