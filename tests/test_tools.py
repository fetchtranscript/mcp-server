"""Tests for MCP tool handlers."""

from __future__ import annotations

import pytest
from mcp.server.fastmcp.exceptions import ToolError
import respx

from fetchtranscript_mcp.client import FetchTranscriptClient
from fetchtranscript_mcp.tools import register_tools

from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.fetchtranscript.com"


@pytest.fixture
def mcp_server():
    """Create a FastMCP instance with tools registered."""
    client = FetchTranscriptClient(api_key="yt_test", base_url=BASE_URL)
    server = FastMCP("test")
    register_tools(server, lambda: client)
    return server


@pytest.mark.asyncio
async def test_get_transcript_text(mcp_server: FastMCP):
    with respx.mock(base_url=BASE_URL) as router:
        router.get("/v1/transcripts/abc12345678", params={"format": "text"}).respond(
            200,
            json={
                "video_id": "abc12345678",
                "language": "en",
                "text": "Hello world transcript",
                "segments": [],
                "is_generated": False,
                "provider": "custom",
                "metadata": {"title": "Test Video", "author": "Author"},
            },
        )
        # Call the tool function directly
        tools = mcp_server._tool_manager._tools
        result = await tools["get_transcript"].fn(video_id="abc12345678")
        assert "Test Video" in result
        assert "Hello world transcript" in result


@pytest.mark.asyncio
async def test_get_transcript_error(mcp_server: FastMCP):
    with respx.mock(base_url=BASE_URL) as router:
        router.get("/v1/transcripts/notfound1234", params={"format": "text"}).respond(
            404,
            json={"error": "video_not_found", "message": "Video not found"},
        )
        tools = mcp_server._tool_manager._tools
        with pytest.raises(ToolError, match="Video not found"):
            await tools["get_transcript"].fn(video_id="notfound1234")


@pytest.mark.asyncio
async def test_list_languages(mcp_server: FastMCP):
    with respx.mock(base_url=BASE_URL) as router:
        router.get("/v1/transcripts/abc12345678/languages").respond(
            200,
            json={
                "video_id": "abc12345678",
                "languages": [
                    {"language_code": "en", "language": "English", "is_generated": False, "is_translatable": True},
                    {"language_code": "it", "language": "Italian", "is_generated": True, "is_translatable": True},
                ],
            },
        )
        tools = mcp_server._tool_manager._tools
        result = await tools["list_languages"].fn(video_id="abc12345678")
        assert "English" in result
        assert "Italian" in result
        assert "(auto-generated)" in result


@pytest.mark.asyncio
async def test_search_videos(mcp_server: FastMCP):
    with respx.mock(base_url=BASE_URL) as router:
        router.get("/v1/search", params={"q": "python", "limit": 5}).respond(
            200,
            json={
                "query": "python",
                "results": [
                    {"video_id": "vid123456789", "title": "Python Tutorial", "channel_name": "Coder", "view_count": 1000},
                ],
                "total_results": 1,
            },
        )
        tools = mcp_server._tool_manager._tools
        result = await tools["search_videos"].fn(query="python")
        assert "Python Tutorial" in result
        assert "Coder" in result


@pytest.mark.asyncio
async def test_get_chapters_no_chapters(mcp_server: FastMCP):
    with respx.mock(base_url=BASE_URL) as router:
        router.get("/v1/videos/abc12345678/chapters").respond(
            200,
            json={"video_id": "abc12345678", "chapters": [], "has_chapters": False},
        )
        tools = mcp_server._tool_manager._tools
        result = await tools["get_chapters"].fn(video_id="abc12345678")
        assert "no chapters" in result.lower()
