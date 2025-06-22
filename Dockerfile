FROM ghcr.io/astral-sh/uv:python3.13-bookworm-slim AS python

ENV PYTHONUNBUFFERED=true
LABEL org.opencontainers.image.source="https://github.com/lanterno/remote_python"
LABEL authors="ahmed.elghareeb@proton.com"

WORKDIR /deps

COPY pyproject.toml ./
COPY uv.lock ./

RUN uv sync --locked

ENV PATH="/deps/.venv/bin:$PATH"

WORKDIR /app

COPY . ./

EXPOSE 8080

CMD ["uvicorn", "server:app", "--host", "0.0.0.0", "--port", "8080"]
