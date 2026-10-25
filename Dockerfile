FROM python:3.10-slim

WORKDIR /app

COPY code_context_mcp.py /app/
COPY pyproject.toml /app/

ENTRYPOINT ["python", "code_context_mcp.py"]
