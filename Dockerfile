# Management Tools Analysis Dashboard
# Root-level Dockerfile for Dokploy deployment
# The actual app lives in dashboard_app/

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1

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

# Install pip dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the full dashboard_app source
COPY dashboard_app/ .

# Create necessary directories
RUN mkdir -p data logs assets

# Copy .env.example as .env template (real secrets injected via Dokploy env vars)
RUN if [ -f .env.example ]; then cp .env.example .env; fi

# Expose the Dash port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=15s --retries=3 \
    CMD curl -f http://localhost:8050/ || exit 1

# Start the application
CMD ["python", "app.py"]
