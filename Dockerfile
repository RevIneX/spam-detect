FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip install --no-cache-dir \
    torch==2.1.0 \
    transformers==4.35.0 \
    numpy==1.26.0
COPY requirements.txt .
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install -r requirements.txt
COPY ./app ./app
ENV PYTHONPATH=/app
EXPOSE 1001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1001"]