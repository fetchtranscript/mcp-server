# Installing the FetchTranscript MCP server (for AI agents)

The server runs locally over stdio and is published on PyPI as `fetchtranscript-mcp`.

## 1. Requirements

- `uv` (provides `uvx`): `curl -LsSf https://astral.sh/uv/install.sh | sh` (or `brew install uv`). Alternatively Python 3.10+ and `pip install fetchtranscript-mcp`.
- A FetchTranscript API key (starts with `yt_`). Ask the user for it; they can create one for free (25 calls/month) at https://fetchtranscript.com/dashboard/api-keys. Never invent a key.

## 2. MCP client configuration

Add this server to the client's MCP settings (for Cline: `cline_mcp_settings.json`), replacing the key:

```json
{
  "mcpServers": {
    "fetchtranscript": {
      "command": "uvx",
      "args": ["fetchtranscript-mcp"],
      "env": {
        "FETCHTRANSCRIPT_API_KEY": "yt_your_api_key"
      }
    }
  }
}
```

Without uv, use `"command": "fetchtranscript-mcp"` after `pip install fetchtranscript-mcp`.

## 3. Check it works

After the client restarts the server it should list 8 tools: `get_transcript`, `list_languages`, `get_video_metadata`, `get_chapters`, `get_comments`, `get_channel_info`, `list_channel_videos`, `search_videos`. Try `get_transcript` with `video_id` `dQw4w9WgXcQ`.

An `Invalid or inactive API key` error means the key is wrong or revoked; `Insufficient credits` means the free calls are used up (top up at https://fetchtranscript.com/dashboard/billing).
