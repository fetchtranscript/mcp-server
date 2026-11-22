"""Async HTTP client for the FetchTranscript REST API."""

from __future__ import annotations

from typing import Any

import httpx

from .errors import raise_for_status

DEFAULT_BASE_URL = "https://api.fetchtranscript.com"
DEFAULT_TIMEOUT = 30.0


class FetchTranscriptClient:
    """Async wrapper around the FetchTranscript REST API."""

    def __init__(self, api_key: str, base_url: str = DEFAULT_BASE_URL):
        self._client = httpx.AsyncClient(
            base_url=base_url.rstrip("/"),
            headers={
                "X-API-Key": api_key,
                "User-Agent": "FetchTranscript-MCP/0.1.1",
            },
            timeout=DEFAULT_TIMEOUT,
        )

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> dict[str, Any]:
        response = await self._client.get(path, params=params)
        raise_for_status(response)
        return response.json()

    # -- Transcripts --

    async def get_transcript(
        self,
        video_id: str,
        lang: str | None = None,
        format: str | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if lang:
            params["lang"] = lang
        if format:
            params["format"] = format
        return await self._get(f"/v1/transcripts/{video_id}", params or None)

    async def list_languages(self, video_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/transcripts/{video_id}/languages")

    # -- Videos --

    async def get_video_metadata(self, video_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/videos/{video_id}")

    async def get_chapters(self, video_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/videos/{video_id}/chapters")

    async def get_comments(
        self, video_id: str, limit: int | None = None, sort: str | None = None
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if sort is not None:
            params["sort"] = sort
        return await self._get(f"/v1/videos/{video_id}/comments", params or None)

    # -- Channels --

    async def get_channel_info(self, channel_id: str) -> dict[str, Any]:
        return await self._get(f"/v1/channels/{channel_id}")

    async def list_channel_videos(
        self,
        channel_id: str,
        limit: int | None = None,
        offset: int | None = None,
        include_shorts: bool | None = None,
    ) -> dict[str, Any]:
        params: dict[str, Any] = {}
        if limit is not None:
            params["limit"] = limit
        if offset is not None:
            params["offset"] = offset
        if include_shorts is not None:
            params["include_shorts"] = include_shorts
        return await self._get(f"/v1/channels/{channel_id}/videos", params or None)

    # -- Search --

    async def search_videos(self, query: str, limit: int | None = None) -> dict[str, Any]:
        params: dict[str, Any] = {"q": query}
        if limit is not None:
            params["limit"] = limit
        return await self._get("/v1/search", params)

    async def close(self) -> None:
        await self._client.aclose()
