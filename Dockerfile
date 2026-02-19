# Management Tools Analysis Dashboard
# Root-level Dockerfile for Dokploy deployment
# The actual app lives in dashboard_app/

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV FLASK_ENV=production
ENV DASH_DEBUG=false

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    gfortran \
    curl \
    pkg-config \
    libopenblas-dev \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy only the dashboard_app directory contents
COPY dashboard_app/requirements.txt ./
COPY dashboard_app/pyproject.toml dashboard_app/uv.lock ./

# Upgrade pip first so it can resolve ARM64 binary wheels properly
RUN pip install --upgrade pip

# Stage 1: Install heavy scientific packages using ARM64 binary wheels.
# Pinned versions in requirements.txt (numpy 2.3.3, pandas 2.3.3) have NO
# aarch64 wheels on PyPI, forcing source compilation that times out.
# These slightly older versions are fully compatible and have ARM64 wheels.
RUN pip install --no-cache-dir --only-binary=all \
    "numpy>=1.26,<2.3" \
    "pandas>=2.2,<2.3" \
    "scipy>=1.13" \
    "scikit-learn>=1.5"

# Stage 2: Install remaining packages (excluding already-installed heavy ones)
RUN grep -vE "^(numpy|pandas|scipy|scikit.learn)==" requirements.txt \
    > /tmp/req_filtered.txt && \
    pip install --no-cache-dir --prefer-binary -r /tmp/req_filtered.txt

# Copy the full dashboard_app source
COPY dashboard_app/ .

# Create necessary directories
RUN mkdir -p data logs assets

# Copy .env.example as .env template (real secrets injected via Dokploy env vars)
RUN if [ -f .env.example ]; then cp .env.example .env; fi

# Expose the Dash port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=60s --retries=5 \
    CMD curl -f http://localhost:8050/ || exit 1

# Start the application
CMD ["python", "app.py", "--port", "8050"]
