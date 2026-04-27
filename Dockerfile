# syntax=docker/dockerfile:1
FROM python:3.11-slim AS builder
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc libpq-dev && rm -rf /var/lib/apt/lists/*
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --link-mode=copy --system \
    torch==2.4.0 --index-url https://download.pytorch.org/whl/cpu
COPY requirements-ml.txt requirements.txt ./
RUN --mount=type=cache,target=/root/.cache/uv \
    uv pip install --link-mode=copy --system \
    -r requirements-ml.txt -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq5 && rm -rf /var/lib/apt/lists/* \
    && useradd -m slowpoke
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin
RUN chown -R slowpoke /app
COPY --chown=slowpoke:slowpoke ./app ./app
ENV PYTHONPATH=/app PYTHONUNBUFFERED=1
USER slowpoke
EXPOSE 1001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1001"]
