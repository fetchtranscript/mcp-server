"""MCP prompt templates for common YouTube transcript workflows."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register_prompts(mcp: FastMCP) -> None:
    """Register prompt templates on the MCP server."""

    @mcp.prompt()
    async def summarize_video(video_id: str, lang: str | None = None) -> str:
        """Summarize a YouTube video from its transcript.

        Args:
            video_id: YouTube video ID (e.g. 'dQw4w9WgXcQ')
            lang: Transcript language code (optional, auto-detected if omitted)
        """
        lang_instruction = f" in {lang}" if lang else ""
        return (
            f"Please summarize the YouTube video with ID `{video_id}`.\n\n"
            f"Steps:\n"
            f"1. First, call `get_video_metadata` for `{video_id}` to get the title and context.\n"
            f"2. Then, call `get_transcript` for `{video_id}`{lang_instruction} to get the full text.\n"
            f"3. Provide a structured summary with:\n"
            f"   - **Title and channel**\n"
            f"   - **Key points** (bulleted list)\n"
            f"   - **Main takeaways** (2-3 sentences)\n"
            f"   - **Notable quotes** (if any)\n"
        )

    @mcp.prompt()
    async def compare_videos(video_ids: str) -> str:
        """Compare multiple YouTube videos on similar topics.

        Args:
            video_ids: Comma-separated list of video IDs (e.g. 'abc123,def456,ghi789')
        """
        ids = [v.strip() for v in video_ids.split(",") if v.strip()]
        id_list = ", ".join(f"`{v}`" for v in ids)
        return (
            f"Please compare these YouTube videos: {id_list}.\n\n"
            f"Steps:\n"
            f"1. For each video, call `get_video_metadata` to get the title and context.\n"
            f"2. For each video, call `get_transcript` to get the full text.\n"
            f"3. Provide a comparison covering:\n"
            f"   - **Topics covered** by each video\n"
            f"   - **Key differences** in perspective or approach\n"
            f"   - **Common themes** across all videos\n"
            f"   - **Which video is best for** different audiences or goals\n"
        )

    @mcp.prompt()
    async def extract_quotes(video_id: str, topic: str | None = None) -> str:
        """Extract notable quotes from a YouTube video.

        Args:
            video_id: YouTube video ID
            topic: Optional topic to focus on (e.g. 'machine learning', 'productivity')
        """
        topic_filter = f" related to **{topic}**" if topic else ""
        return (
            f"Please extract key quotes from YouTube video `{video_id}`{topic_filter}.\n\n"
            f"Steps:\n"
            f"1. Call `get_video_metadata` for `{video_id}` to get the title.\n"
            f"2. Call `get_transcript` for `{video_id}` with `format=\"json\"` to get timestamped segments.\n"
            f"3. Identify the most notable, insightful, or impactful quotes{topic_filter}.\n"
            f"4. Present each quote as:\n"
            f"   - **[MM:SS]** \"quote text\"\n"
            f"   - Brief context of why this quote is notable\n"
            f"\nAim for 5-10 quotes that best represent the video's content.\n"
        )
