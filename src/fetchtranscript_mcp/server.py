"""FetchTranscript MCP Server entry point."""

from __future__ import annotations

import os
import sys

from mcp.server.fastmcp import FastMCP

from .client import FetchTranscriptClient
from .prompts import register_prompts
from .resources import register_resources
from .tools import register_tools

mcp = FastMCP(
    "FetchTranscript",
    instructions="Access YouTube transcripts, video metadata, chapters, comments, channels, and search via the FetchTranscript API.",
)

# Lazy-init client so import doesn't fail without env var (tests, --help, etc.)
_client: FetchTranscriptClient | None = None


def _get_client() -> FetchTranscriptClient:
    global _client
    if _client is None:
        api_key = os.environ.get("FETCHTRANSCRIPT_API_KEY", "")
        if not api_key:
            print(
                "Error: FETCHTRANSCRIPT_API_KEY environment variable is required.\n"
                "Get your API key at https://fetchtranscript.com",
                file=sys.stderr,
            )
            sys.exit(1)
        base_url = os.environ.get(
            "FETCHTRANSCRIPT_BASE_URL", "https://api.fetchtranscript.com"
        )
        _client = FetchTranscriptClient(api_key=api_key, base_url=base_url)
    return _client


# Register components — tools get a lazy client reference
register_tools(mcp, _get_client)  # type: ignore[arg-type]
register_resources(mcp)
register_prompts(mcp)


def main() -> None:
    """Run the MCP server (stdio transport)."""
    # Force client init to fail fast if key is missing
    _get_client()
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
