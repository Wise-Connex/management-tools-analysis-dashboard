# Management Tools Analysis Dashboard - Production Dockerfile
# Phase 5: Production Deployment & Monitoring

FROM python:3.11-slim

# Set environment variables
ENV PYTHONUNBUFFERED=1
ENV PYTHONDONTWRITEBYTECODE=1
ENV UV_COMPILE_BYTECODE=1
ENV UV_LINK_MODE=copy

# Install system dependencies
RUN apt-get update && apt-get install -y \
    gcc \
    g++ \
    curl \
    wget \
    && rm -rf /var/lib/apt/lists/*

# Create app user and directory
RUN groupadd -r appuser && useradd -r -g appuser appuser
RUN mkdir -p /app && chown -R appuser:appuser /app

# Set working directory
WORKDIR /app

# Copy requirements and uv files
COPY pyproject.toml uv.lock ./
COPY requirements.txt ./

# Install uv package manager
RUN pip install uv

# Install Python dependencies using uv
RUN uv pip install --system -r requirements.txt

# Copy application code
COPY . .

# Create necessary directories
RUN mkdir -p data logs assets && \
    chown -R appuser:appuser data logs assets

# Copy environment file template
COPY .env.example .env

# Make entrypoint executable
COPY docker/entrypoint.sh /entrypoint.sh
RUN chmod +x /entrypoint.sh

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8050

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8050/ || exit 1

# Set startup command
ENTRYPOINT ["/entrypoint.sh"]
CMD ["python", "app.py"]