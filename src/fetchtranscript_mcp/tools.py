"""MCP tool definitions for FetchTranscript."""

from __future__ import annotations

import json
from collections.abc import Callable

from mcp.server.fastmcp import FastMCP
from mcp.server.fastmcp.exceptions import ToolError

from .client import FetchTranscriptClient
from .errors import FetchTranscriptError


def register_tools(mcp: FastMCP, get_client: Callable[[], FetchTranscriptClient]) -> None:
    """Register all tools on the MCP server instance.

    API errors are raised as ToolError, so the client sees a failed call (isError) with the
    API's message, not a successful result that reads like a transcript.
    """

    @mcp.tool()
    async def get_transcript(
        video_id: str,
        lang: str | None = None,
        format: str = "text",
    ) -> str:
        """Get the transcript of a YouTube video.

        Args:
            video_id: YouTube video ID (11 characters, e.g. 'dQw4w9WgXcQ')
            lang: Language code (e.g. 'en', 'it'). Auto-detected if omitted.
            format: Output format — 'text' (default), 'json' (segments with timestamps), or 'srt'.
        """
        try:
            data = await get_client().get_transcript(video_id, lang=lang, format=format)
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        if format == "text" and data.get("text"):
            lines = []
            meta = data.get("metadata")
            if meta:
                lines.append(f"**{meta['title']}** by {meta['author']}")
                lines.append("")
            lines.append(data["text"])
            return "\n".join(lines)

        return json.dumps(data, indent=2)

    @mcp.tool()
    async def list_languages(video_id: str) -> str:
        """List available transcript languages for a YouTube video.

        Args:
            video_id: YouTube video ID (11 characters)
        """
        try:
            data = await get_client().list_languages(video_id)
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        langs = data.get("languages", [])
        if not langs:
            return "No transcripts available for this video."

        lines = [f"Available languages for {video_id}:"]
        for lang in langs:
            tag = " (auto-generated)" if lang.get("is_generated") else ""
            lines.append(f"- {lang['language']} ({lang['language_code']}){tag}")
        return "\n".join(lines)

    @mcp.tool()
    async def get_video_metadata(video_id: str) -> str:
        """Get metadata for a YouTube video (title, description, views, likes, etc.).

        Args:
            video_id: YouTube video ID (11 characters)
        """
        try:
            data = await get_client().get_video_metadata(video_id)
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        lines = [
            f"**{data.get('title', 'Unknown')}**",
            f"Channel: {data.get('channel_name', 'Unknown')}",
            f"Views: {data.get('view_count', 'N/A'):,}" if isinstance(data.get('view_count'), int) else f"Views: {data.get('view_count', 'N/A')}",
            f"Likes: {data.get('like_count', 'N/A'):,}" if isinstance(data.get('like_count'), int) else f"Likes: {data.get('like_count', 'N/A')}",
            f"Duration: {data.get('duration', 'N/A')}s",
            f"Upload date: {data.get('upload_date', 'N/A')}",
        ]
        desc = data.get("description")
        if desc:
            lines.append(f"\nDescription:\n{desc}")
        tags = data.get("tags", [])
        if tags:
            lines.append(f"\nTags: {', '.join(tags)}")
        return "\n".join(lines)

    @mcp.tool()
    async def get_chapters(video_id: str) -> str:
        """Get chapter list for a YouTube video.

        Args:
            video_id: YouTube video ID (11 characters)
        """
        try:
            data = await get_client().get_chapters(video_id)
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        if not data.get("has_chapters"):
            return "This video has no chapters."

        lines = [f"Chapters for {video_id}:"]
        for ch in data.get("chapters", []):
            start = int(ch["start_time"])
            mm, ss = divmod(start, 60)
            lines.append(f"- [{mm}:{ss:02d}] {ch['title']}")
        return "\n".join(lines)

    @mcp.tool()
    async def get_comments(video_id: str, limit: int = 20, sort: str = "top") -> str:
        """Get the top-level comments of a YouTube video, each with its like and reply count.

        Costs 1 credit per 100 comments returned, rounded up (minimum 1): up to 100 comments
        cost 1 credit, 101-200 cost 2. Videos with comments turned off cost nothing.

        Args:
            video_id: YouTube video ID (11 characters)
            limit: Number of comments to fetch (default 20, max 500)
            sort: "top" (default) or "new" (newest first)
        """
        try:
            data = await get_client().get_comments(video_id, limit=limit, sort=sort)
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        comments = data.get("comments", [])
        if not comments:
            return "No comments found for this video."

        lines = [f"Comments for {video_id} ({data.get('total_count', '?')} total):"]
        for c in comments:
            likes = f" [{c['like_count']} likes]" if c.get("like_count") else ""
            pinned = " (pinned)" if c.get("is_pinned") else ""
            lines.append(f"- **{c['author']}**{pinned}{likes}: {c['text']}")
        if data.get("has_more"):
            lines.append(f"\n({len(comments)} shown, more available)")
        return "\n".join(lines)

    @mcp.tool()
    async def get_channel_info(channel_id: str) -> str:
        """Get information about a YouTube channel.

        Args:
            channel_id: YouTube channel ID (UCxxxxxx format) or handle (@username)
        """
        try:
            data = await get_client().get_channel_info(channel_id)
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        subs = data.get("subscriber_count")
        subs_str = f"{subs:,}" if isinstance(subs, int) else "N/A"
        lines = [
            f"**{data.get('name', 'Unknown')}**",
            f"Subscribers: {subs_str}",
            f"Videos: {data.get('video_count', 'N/A')}",
            f"URL: {data.get('channel_url', 'N/A')}",
        ]
        desc = data.get("description")
        if desc:
            lines.append(f"\n{desc}")
        return "\n".join(lines)

    @mcp.tool()
    async def list_channel_videos(
        channel_id: str,
        limit: int = 10,
        offset: int = 0,
        include_shorts: bool = False,
    ) -> str:
        """List videos from a YouTube channel.

        Args:
            channel_id: YouTube channel ID (UCxxxxxx format) or handle (@username)
            limit: Number of videos to return (default 10, max 100)
            offset: Number of videos to skip for pagination (default 0)
            include_shorts: Whether to include YouTube Shorts (default false)
        """
        try:
            data = await get_client().list_channel_videos(
                channel_id, limit=limit, offset=offset, include_shorts=include_shorts
            )
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        videos = data.get("videos", [])
        if not videos:
            return "No videos found for this channel."

        total = data.get("total_count")
        header = f"Videos from channel ({total} total):" if total else "Videos from channel:"
        lines = [header]
        for v in videos:
            views = f" — {v['view_count']:,} views" if isinstance(v.get("view_count"), int) else ""
            lines.append(f"- [{v['video_id']}] {v['title']}{views}")
        if data.get("has_more"):
            lines.append(f"\n(showing {offset + 1}–{offset + len(videos)}, more available)")
        return "\n".join(lines)

    @mcp.tool()
    async def search_videos(query: str, limit: int = 5) -> str:
        """Search YouTube videos.

        Args:
            query: Search query string
            limit: Number of results (default 5, max 50)
        """
        try:
            data = await get_client().search_videos(query, limit=limit)
        except FetchTranscriptError as e:
            raise ToolError(e.message) from e

        results = data.get("results", [])
        if not results:
            return f"No results found for '{query}'."

        lines = [f"Search results for '{query}':"]
        for r in results:
            channel = f" by {r['channel_name']}" if r.get("channel_name") else ""
            views = f" ({r['view_count']:,} views)" if isinstance(r.get("view_count"), int) else ""
            lines.append(f"- [{r['video_id']}] {r['title']}{channel}{views}")
        return "\n".join(lines)
