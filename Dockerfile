# Management Tools Analysis Dashboard
# Single-stage build optimized for low-disk ARM64 servers (Dokploy)
# All Python packages installed as pre-built binary wheels — no compiler needed.

FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV DASH_DEBUG=false

# Runtime dependency only — curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copy requirements first for layer caching
COPY dashboard_app/requirements.txt ./

# Install all packages as binary wheels in a single step.
# --only-binary=:all: ensures no source compilation (no gcc needed).
# Strip hashes from uv-exported requirements to avoid platform mismatches.
RUN sed 's/ *\\$//; /^[[:space:]]*--hash/d; /^[[:space:]]*#/d; /^$/d' requirements.txt \
    > /tmp/req_clean.txt && \
    pip install --no-cache-dir --only-binary=:all: -r /tmp/req_clean.txt && \
    rm -f /tmp/req_clean.txt requirements.txt

# Copy the full source code (respecting .dockerignore)
COPY . .

WORKDIR /app/dashboard_app

# Create necessary directories
RUN mkdir -p data logs assets

# Copy .env.example as .env template (real secrets injected via Dokploy env vars)
RUN if [ -f ../.env.example ]; then cp ../.env.example .env; fi

EXPOSE 8050

HEALTHCHECK --interval=30s --timeout=15s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:8050/ || exit 1

CMD ["python", "app.py", "--port", "8050"]
