"""Shared fixtures for MCP server tests."""

from __future__ import annotations

import pytest
import respx

from fetchtranscript_mcp.client import FetchTranscriptClient

BASE_URL = "https://api.fetchtranscript.com"


@pytest.fixture
def mock_api():
    """respx mock router scoped to the FetchTranscript base URL."""
    with respx.mock(base_url=BASE_URL) as router:
        yield router


@pytest.fixture
def client():
    """FetchTranscriptClient pointed at the mocked base URL."""
    return FetchTranscriptClient(api_key="yt_test_key", base_url=BASE_URL)
