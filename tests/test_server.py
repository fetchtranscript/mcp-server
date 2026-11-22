"""Integration tests — verify the MCP server registers all components."""

from __future__ import annotations

import os
from unittest.mock import patch

import pytest

from mcp.server.fastmcp import FastMCP


@pytest.fixture
def server():
    """Import server module with a fake API key set."""
    with patch.dict(os.environ, {"FETCHTRANSCRIPT_API_KEY": "yt_test_integration"}):
        # Re-import to pick up the env var
        import importlib
        import fetchtranscript_mcp.server as srv_mod

        importlib.reload(srv_mod)
        yield srv_mod.mcp


def test_server_has_tools(server: FastMCP):
    tools = server._tool_manager._tools
    expected = {
        "get_transcript",
        "list_languages",
        "get_video_metadata",
        "get_chapters",
        "get_comments",
        "get_channel_info",
        "list_channel_videos",
        "search_videos",
    }
    assert expected.issubset(set(tools.keys())), f"Missing tools: {expected - set(tools.keys())}"


def test_server_has_resources(server: FastMCP):
    resources = server._resource_manager._resources
    expected_uris = {
        "fetchtranscript://docs/api-reference",
        "fetchtranscript://docs/quickstart",
        "fetchtranscript://docs/pricing",
        "fetchtranscript://docs/examples",
    }
    actual_uris = set(str(k) for k in resources.keys())
    assert expected_uris.issubset(actual_uris), f"Missing resources: {expected_uris - actual_uris}"


def test_server_has_prompts(server: FastMCP):
    prompts = server._prompt_manager._prompts
    expected = {"summarize_video", "compare_videos", "extract_quotes"}
    assert expected.issubset(set(prompts.keys())), f"Missing prompts: {expected - set(prompts.keys())}"
