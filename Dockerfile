FROM python:3.12-slim

WORKDIR /app

# PostgreSQL client provides pg_isready for the startup readiness check.
RUN apt-get -o Acquire::Retries=5 update \
    && apt-get install -y --no-install-recommends postgresql-client ca-certificates \
    && rm -rf /var/lib/apt/lists/*

# Keep dependency installation in its own cacheable layer.
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade pip \
    && pip install --no-cache-dir -r requirements.txt

COPY . .
RUN chmod +x /app/scripts/entrypoint.sh

ENTRYPOINT ["/app/scripts/entrypoint.sh"]
