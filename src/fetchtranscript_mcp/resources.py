"""MCP resource definitions — static documentation exposed to AI clients."""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP


def register_resources(mcp: FastMCP) -> None:
    """Register documentation resources on the MCP server."""

    @mcp.resource("fetchtranscript://docs/api-reference")
    async def api_reference() -> str:
        """Complete FetchTranscript API reference."""
        return API_REFERENCE

    @mcp.resource("fetchtranscript://docs/quickstart")
    async def quickstart() -> str:
        """Getting started with FetchTranscript MCP server."""
        return QUICKSTART

    @mcp.resource("fetchtranscript://docs/pricing")
    async def pricing() -> str:
        """FetchTranscript pricing and credit system."""
        return PRICING

    @mcp.resource("fetchtranscript://docs/examples")
    async def examples() -> str:
        """Common workflow examples."""
        return EXAMPLES


# ---------------------------------------------------------------------------
# Static content
# ---------------------------------------------------------------------------

API_REFERENCE = """\
# FetchTranscript API Reference

Base URL: `https://api.fetchtranscript.com`

Authentication: `X-API-Key: yt_xxx` header or `Authorization: Bearer yt_xxx`.

Every endpoint costs **1 credit** per call (even cache hits), except comments: **1 credit per \
100 comments returned, rounded up (minimum 1)**. Failed requests (4xx/5xx) cost 0 credits.

---

## Transcripts

### GET /v1/transcripts/{video_id}
Fetch the transcript of a YouTube video.

| Parameter | Type   | Default | Description |
|-----------|--------|---------|-------------|
| video_id  | path   | —       | 11-char YouTube video ID |
| lang      | query  | auto    | Language code (e.g. `en`, `it`) |
| format    | query  | `json`  | `json` (segments), `text` (plain), `srt` |

**Response (json format):**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "language": "en",
  "segments": [{"text": "...", "start": 0.0, "duration": 2.5}],
  "is_generated": false,
  "provider": "youtube_transcript_api",
  "metadata": {
    "title": "...", "author": "...", "thumbnail": "...",
    "length_seconds": 212, "view_count": 1400000000,
    "short_description": "..."
  }
}
```

### GET /v1/transcripts/{video_id}/languages
List available transcript languages.

**Response:**
```json
{
  "video_id": "dQw4w9WgXcQ",
  "languages": [
    {"language_code": "en", "language": "English", "is_generated": false, "is_translatable": true}
  ]
}
```

---

## Videos

### GET /v1/videos/{video_id}
Get video metadata.

**Response:** `video_id`, `title`, `description`, `channel_id`, `channel_name`, `duration`, \
`view_count`, `like_count`, `comment_count`, `upload_date`, `thumbnail_url`, `tags`, `categories`.

### GET /v1/videos/{video_id}/chapters
Get video chapters.

**Response:** `video_id`, `chapters` (list of `{title, start_time, end_time}`), `has_chapters`.

### GET /v1/videos/{video_id}/comments
Get the top-level comments (no replies; each comment has its `reply_count`).
Costs 1 credit per 100 comments returned, rounded up (minimum 1).

| Parameter | Type  | Default | Description               |
|-----------|-------|---------|---------------------------|
| limit     | query | 100     | 1–500                     |
| sort      | query | top     | `top` or `new` (newest)   |

**Response:** `video_id`, `comments` (list of `{comment_id, text, author, author_id, like_count, \
reply_count, published_at, is_pinned}`), `total_count` (the video's comment count as YouTube \
shows it, replies included), `has_more`. `published_at` is an ISO-8601 UTC estimate (YouTube \
only shows "3 days ago"). Comments turned off: 404 `comments_disabled` (free).

---

## Channels

### GET /v1/channels/{channel_id}
Get channel metadata. Accepts `UCxxxxxx` or `@handle` format.

**Response:** `channel_id`, `name`, `description`, `subscriber_count`, `video_count`, \
`thumbnail_url`, `channel_url`.

### GET /v1/channels/{channel_id}/videos
List channel videos.

| Parameter      | Type  | Default | Description |
|----------------|-------|---------|-------------|
| limit          | query | 30      | 1–100       |
| offset         | query | 0       | Pagination  |
| include_shorts | query | false   | Include Shorts |

**Response:** `channel_id`, `videos` (list), `total_count`, `offset`, `limit`, `has_more`.

---

## Search

### GET /v1/search
Search YouTube videos.

| Parameter | Type  | Default | Description |
|-----------|-------|---------|-------------|
| q         | query | —       | Search query (1–500 chars) |
| limit     | query | 10      | 1–50        |

**Response:** `query`, `results` (list of `{video_id, title, channel_name, duration, view_count, ...}`), \
`total_results`.

---

## Error Codes

| Code | HTTP | Meaning |
|------|------|---------|
| `invalid_video_id` | 400 | Video ID is not 11 characters |
| `invalid_channel_id` | 400 | Invalid channel ID or handle |
| `missing_api_key` | 401 | No API key provided |
| `invalid_api_key` | 401 | API key is invalid or inactive |
| `insufficient_credits` | 402 | No credits remaining |
| `video_not_found` | 404 | Video does not exist or is private |
| `transcripts_disabled` | 404 | Video has transcripts disabled |
| `no_transcript_found` | 404 | No transcript in requested language |
| `channel_not_found` | 404 | Channel does not exist |
| `service_unavailable` | 503 | Upstream YouTube error |

Error response format:
```json
{"error": "<code>", "message": "<human-readable>"}
```

## Response Headers
- `X-Credits-Remaining` — credits left after the request
- `X-Processing-Time` — processing time in milliseconds
"""

QUICKSTART = """\
# FetchTranscript MCP — Quick Start

## 1. Get an API Key

Sign up at https://fetchtranscript.com and create an API key from the dashboard.
Keys start with `yt_`.

## 2. Configure your MCP client

### Claude Desktop / Claude Code

Add to your MCP settings (`claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "fetchtranscript": {
      "command": "uvx",
      "args": ["fetchtranscript-mcp"],
      "env": {
        "FETCHTRANSCRIPT_API_KEY": "yt_your_key_here"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json` in your project:

```json
{
  "mcpServers": {
    "fetchtranscript": {
      "command": "uvx",
      "args": ["fetchtranscript-mcp"],
      "env": {
        "FETCHTRANSCRIPT_API_KEY": "yt_your_key_here"
      }
    }
  }
}
```

## 3. Try it out

Ask your AI assistant:
- "Get the transcript of this YouTube video: dQw4w9WgXcQ"
- "What languages are available for video XYZ?"
- "Search YouTube for 'python async tutorial'"

## Alternative: npm wrapper

```bash
npx @fetchtranscript/mcp-server
```

Set `FETCHTRANSCRIPT_API_KEY` as an environment variable.

## Alternative: pip install

```bash
pip install fetchtranscript-mcp
FETCHTRANSCRIPT_API_KEY=yt_xxx fetchtranscript-mcp
```
"""

PRICING = """\
# FetchTranscript Pricing

## Free Tier
- **25 credits/month** — no credit card required
- Resets on the 1st of each month

## Credit Cost
- Every successful API call costs **1 credit**: transcripts, languages, metadata, chapters, \
channels, channel videos, search
- **Comments**: 1 credit per 100 comments returned, rounded up (minimum 1): up to 100 comments \
cost 1 credit, 101-200 cost 2, 500 cost 5
- **Cache hits also cost 1 credit** (transcripts are cached for 30 days)

## What's Free
- **Failed requests cost 0 credits** — if you get a 4xx or 5xx error, you are not charged
- Health check endpoint (`/health`) requires no authentication

## Purchasing Credits
Visit https://fetchtranscript.com/pricing to purchase additional credits.
Credits never expire.

## Checking Your Balance
After each API call, check the `X-Credits-Remaining` response header.
"""

EXAMPLES = """\
# FetchTranscript — Common Workflows

## Summarize a Video
1. Use `get_video_metadata` to get the title and description
2. Use `get_transcript` to get the full text
3. Summarize the transcript, referencing the video title

## Compare Multiple Videos
1. Use `search_videos` to find videos on a topic
2. Use `get_transcript` for each video
3. Compare key points, arguments, and perspectives

## Extract Quotes with Timestamps
1. Use `get_transcript` with `format="json"` to get segments with timestamps
2. Filter segments matching the topic
3. Format as `[MM:SS] "quote text"`

## Analyze a Channel
1. Use `get_channel_info` to get channel overview
2. Use `list_channel_videos` to get recent uploads
3. Use `get_video_metadata` on selected videos for deeper analysis

## Research a Topic
1. Use `search_videos` to find relevant content
2. Use `list_languages` to check subtitle availability
3. Use `get_transcript` with specific `lang` for non-English content
4. Use `get_comments` to gauge audience reaction

## Video Chapter Navigation
1. Use `get_chapters` to get the chapter list
2. Use `get_transcript` with `format="json"` for timestamped segments
3. Match segments to chapters for section-by-section analysis
"""
