"""Tests for the async HTTP client."""

from __future__ import annotations

import httpx
import pytest
import respx

from fetchtranscript_mcp.client import FetchTranscriptClient
from fetchtranscript_mcp.errors import (
    InsufficientCreditsError,
    InvalidVideoIdError,
    VideoNotFoundError,
)


@pytest.mark.asyncio
async def test_get_transcript(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/transcripts/dQw4w9WgXcQ", params={"format": "text"}).respond(
        200,
        json={
            "video_id": "dQw4w9WgXcQ",
            "language": "en",
            "text": "Hello world",
            "segments": [],
            "is_generated": False,
            "provider": "custom",
            "metadata": None,
        },
    )
    data = await client.get_transcript("dQw4w9WgXcQ", format="text")
    assert data["video_id"] == "dQw4w9WgXcQ"
    assert data["text"] == "Hello world"


@pytest.mark.asyncio
async def test_list_languages(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/transcripts/dQw4w9WgXcQ/languages").respond(
        200,
        json={
            "video_id": "dQw4w9WgXcQ",
            "languages": [
                {"language_code": "en", "language": "English", "is_generated": False, "is_translatable": True}
            ],
        },
    )
    data = await client.list_languages("dQw4w9WgXcQ")
    assert len(data["languages"]) == 1
    assert data["languages"][0]["language_code"] == "en"


@pytest.mark.asyncio
async def test_get_video_metadata(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/videos/dQw4w9WgXcQ").respond(
        200,
        json={"video_id": "dQw4w9WgXcQ", "title": "Test", "view_count": 100},
    )
    data = await client.get_video_metadata("dQw4w9WgXcQ")
    assert data["title"] == "Test"


@pytest.mark.asyncio
async def test_get_chapters(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/videos/dQw4w9WgXcQ/chapters").respond(
        200,
        json={"video_id": "dQw4w9WgXcQ", "chapters": [], "has_chapters": False},
    )
    data = await client.get_chapters("dQw4w9WgXcQ")
    assert data["has_chapters"] is False


@pytest.mark.asyncio
async def test_get_comments(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/videos/dQw4w9WgXcQ/comments", params={"limit": 5}).respond(
        200,
        json={"video_id": "dQw4w9WgXcQ", "comments": [], "total_count": 0, "has_more": False},
    )
    data = await client.get_comments("dQw4w9WgXcQ", limit=5)
    assert data["comments"] == []


@pytest.mark.asyncio
async def test_get_comments_sort(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    route = mock_api.get("/v1/videos/dQw4w9WgXcQ/comments").respond(
        200,
        json={"video_id": "dQw4w9WgXcQ", "comments": [], "total_count": 0, "has_more": False},
    )
    await client.get_comments("dQw4w9WgXcQ", limit=5, sort="new")
    params = route.calls.last.request.url.params
    assert params["sort"] == "new"
    assert params["limit"] == "5"


@pytest.mark.asyncio
async def test_get_channel_info(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/channels/UCtest").respond(
        200,
        json={"channel_id": "UCtest", "name": "Test Channel", "channel_url": "https://youtube.com/c/test"},
    )
    data = await client.get_channel_info("UCtest")
    assert data["name"] == "Test Channel"


@pytest.mark.asyncio
async def test_list_channel_videos(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/channels/UCtest/videos", params={"limit": 10}).respond(
        200,
        json={"channel_id": "UCtest", "videos": [], "total_count": 0, "offset": 0, "limit": 10, "has_more": False},
    )
    data = await client.list_channel_videos("UCtest", limit=10)
    assert data["videos"] == []


@pytest.mark.asyncio
async def test_search_videos(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/search", params={"q": "test", "limit": 5}).respond(
        200,
        json={"query": "test", "results": [], "total_results": 0},
    )
    data = await client.search_videos("test", limit=5)
    assert data["query"] == "test"


@pytest.mark.asyncio
async def test_video_not_found(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/videos/invalid12345").respond(
        404,
        json={"error": "video_not_found", "message": "Video not found"},
    )
    with pytest.raises(VideoNotFoundError, match="Video not found"):
        await client.get_video_metadata("invalid12345")


@pytest.mark.asyncio
async def test_invalid_video_id(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/videos/bad").respond(
        400,
        json={"error": "invalid_video_id", "message": "Invalid video ID format"},
    )
    with pytest.raises(InvalidVideoIdError):
        await client.get_video_metadata("bad")


@pytest.mark.asyncio
async def test_insufficient_credits(mock_api: respx.MockRouter, client: FetchTranscriptClient):
    mock_api.get("/v1/videos/dQw4w9WgXcQ").respond(
        402,
        json={"error": "insufficient_credits", "message": "Insufficient credits"},
    )
    with pytest.raises(InsufficientCreditsError):
        await client.get_video_metadata("dQw4w9WgXcQ")
