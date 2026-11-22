# Runs the FetchTranscript MCP server over stdio (for registries' automated checks and container use).
# Usage: docker run -i --rm -e FETCHTRANSCRIPT_API_KEY=yt_... fetchtranscript-mcp
FROM python:3.12-slim
WORKDIR /app
COPY pyproject.toml README.md LICENSE ./
COPY src ./src
RUN pip install --no-cache-dir .
ENTRYPOINT ["fetchtranscript-mcp"]
