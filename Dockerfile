FROM python:3.11-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*
RUN pip config set global.index-url https://pypi.org/simple
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY ./app ./app
ENV PYTHONPATH=/app
EXPOSE 1001
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "1001"]