# FetchTranscript MCP Server

<!-- mcp-name: com.fetchtranscript/fetchtranscript -->

[![Listed on mcpservers.org](https://mcpservers.org/badge.svg)](https://mcpservers.org/servers/fetchtranscript/mcp-server)

[![mcptry](https://mcptry.com/badge/com.fetchtranscript/fetchtranscript)](https://mcptry.com/servers/com.fetchtranscript/fetchtranscript)

An [MCP](https://modelcontextprotocol.io) server that gives AI assistants (Claude Desktop, Cursor, etc.) access to YouTube transcripts, video metadata, channels, and search via the [FetchTranscript](https://fetchtranscript.com) API.

## No install: connect from Claude.ai or ChatGPT

FetchTranscript also runs as a **remote MCP server** with OAuth sign-in, so you can use the same tools from
Claude.ai, Claude Desktop and mobile, ChatGPT or any client that supports remote servers, without an API key or
anything to install:

```
https://api.fetchtranscript.com/mcp
```

- **Claude**: Customize → Connectors → + Add → Add custom connector, paste the URL, then sign in with your
  FetchTranscript account and allow access.
- **ChatGPT**: chatgpt.com/plugins → + → Add custom MCP server, paste the URL as Server URL, OAuth authentication.
- **Claude Code**: `claude mcp add --transport http fetchtranscript https://api.fetchtranscript.com/mcp`

Calls use your account's credits exactly like the API. Step-by-step guide: https://fetchtranscript.com/docs/mcp.
The package below is the **local** server (stdio, API key), for developers who prefer to run it themselves; both
offer the same tools, prompts and resources.

## Features

**8 Tools** — get transcripts, list languages, video metadata, chapters, comments, channel info, channel videos, search

**4 Documentation Resources** — API reference, quickstart guide, pricing, workflow examples

**3 Prompt Templates** — summarize video, compare videos, extract quotes

## Quick Start

### 1. Get an API Key

Sign up at [fetchtranscript.com](https://fetchtranscript.com) and create an API key from the dashboard.

### 2. Configure Claude Desktop

Add to your `claude_desktop_config.json`:

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

### 3. Use it

Ask Claude:
- "Get the transcript of YouTube video dQw4w9WgXcQ"
- "Summarize this YouTube video: https://youtube.com/watch?v=..."
- "Search YouTube for 'machine learning explained' and summarize the top result"

## Configuration for Other Clients

### Cursor

Add to `.cursor/mcp.json`:

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

### Claude Code

```bash
claude mcp add fetchtranscript -- uvx fetchtranscript-mcp
```

Set `FETCHTRANSCRIPT_API_KEY` in your environment.

## Installation Alternatives

### pip

```bash
pip install fetchtranscript-mcp
FETCHTRANSCRIPT_API_KEY=yt_xxx fetchtranscript-mcp
```

### npx

```bash
FETCHTRANSCRIPT_API_KEY=yt_xxx npx fetchtranscript-mcp
```

## Tools

| Tool | Description | Key defaults |
|------|-------------|--------------|
| `get_transcript` | Fetch video transcript | format=text |
| `list_languages` | Available transcript languages | — |
| `get_video_metadata` | Video title, views, likes, etc. | — |
| `get_chapters` | Video chapter list | — |
| `get_comments` | Top comments | limit=20 |
| `get_channel_info` | Channel metadata | — |
| `list_channel_videos` | Videos from a channel | limit=10 |
| `search_videos` | Search YouTube | limit=5 |

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `FETCHTRANSCRIPT_API_KEY` | Yes | Your API key (starts with `yt_`) |
| `FETCHTRANSCRIPT_BASE_URL` | No | Override API base URL (default: `https://api.fetchtranscript.com`) |

## Development

```bash
cd mcp
pip install -e ".[dev]"
pytest tests/
```

Test with MCP Inspector:

```bash
FETCHTRANSCRIPT_API_KEY=yt_xxx mcp dev src/fetchtranscript_mcp/server.py
```

## License

MIT
