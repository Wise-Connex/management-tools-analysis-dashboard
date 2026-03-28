# Management Tools Analysis Dashboard
# Root-level Dockerfile for Dokploy deployment
# Multi-stage build to minimize disk usage and final image size

# ── Stage 1: Builder ─────────────────────────────────────────────
FROM python:3.11-slim AS builder

ENV PYTHONDONTWRITEBYTECODE=1

# Minimal build deps — only gcc for packages that need C compilation.
# gfortran and libopenblas-dev are NOT needed: heavy science packages
# (numpy, scipy, etc.) are installed as pre-built binary wheels.
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    g++ \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /build

COPY dashboard_app/requirements.txt ./

RUN pip install --upgrade pip

# Install heavy science packages as binary-only wheels (no compilation needed)
RUN pip install --no-cache-dir --only-binary=:all: \
    "numpy>=1.26,<2.4" \
    "pandas>=2.2,<2.4" \
    "scipy>=1.13" \
    "scikit-learn>=1.5" \
    "statsmodels>=0.14,<0.15" \
    "aiohttp>=3.10,<3.14"

# Install remaining packages (Dash, plotly, etc.)
RUN grep -vE "^(numpy|pandas|scipy|scikit.learn|statsmodels|aiohttp)==" requirements.txt \
    > /tmp/req_filtered.txt && \
    pip install --no-cache-dir --prefer-binary -r /tmp/req_filtered.txt

# ── Stage 2: Runtime ─────────────────────────────────────────────
FROM python:3.11-slim

ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV DASH_DEBUG=false

# Only runtime dependencies — curl for healthcheck
RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Copy installed Python packages from builder
COPY --from=builder /usr/local/lib/python3.11/site-packages /usr/local/lib/python3.11/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

WORKDIR /app

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
