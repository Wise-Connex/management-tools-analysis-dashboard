#!/bin/bash
# Management Tools Analysis Dashboard - Docker Entrypoint Script
# Phase 5: Production Deployment & Monitoring

set -e

echo "🚀 Starting Management Tools Analysis Dashboard..."

# Function to wait for database to be ready
wait_for_db() {
    echo "⏳ Waiting for database initialization..."
    local max_attempts=30
    local attempt=1
    
    while [ $attempt -le $max_attempts ]; do
        if [ -f "database_implementation/precomputed_findings.db" ]; then
            echo "✅ Database file found"
            break
        fi
        echo "⏳ Attempt $attempt/$max_attempts - waiting for database..."
        sleep 2
        attempt=$((attempt + 1))
    done
    
    if [ $attempt -gt $max_attempts ]; then
        echo "❌ Database not found after $max_attempts attempts"
        exit 1
    fi
}

# Function to validate environment
validate_env() {
    echo "🔍 Validating environment configuration..."
    
    # Check if .env exists
    if [ ! -f ".env" ]; then
        echo "⚠️  .env file not found, using .env.example as template"
        if [ -f ".env.example" ]; then
            cp .env.example .env
            echo "📝 Created .env from template"
        fi
    fi
    
    # Create necessary directories
    mkdir -p data logs assets
    
    # Set proper permissions
    chmod 755 data logs assets
    
    echo "✅ Environment validation complete"
}

# Function to setup monitoring
setup_monitoring() {
    echo "📊 Setting up monitoring..."
    
    # Create monitoring directory
    mkdir -p /tmp/monitoring
    
    # Create basic health check endpoint info
    cat > /tmp/monitoring/health.txt << EOF
Dashboard URL: http://localhost:8050/
Health Check: curl -f http://localhost:8050/
Environment: $(uname -a)
Startup Time: $(date)
Container ID: $(hostname)
EOF
    
    echo "✅ Monitoring setup complete"
}

# Function to handle graceful shutdown
graceful_shutdown() {
    echo "🛑 Received shutdown signal, cleaning up..."
    
    # Stop any background processes
    pkill -f "python.*app.py" || true
    
    echo "✅ Shutdown complete"
}

# Trap signals for graceful shutdown
trap graceful_shutdown SIGTERM SIGINT

# Main startup sequence
echo "🔄 Starting dashboard initialization..."

# Validate environment
validate_env

# Wait for database
wait_for_db

# Setup monitoring
setup_monitoring

# Print startup information
echo ""
echo "=========================================="
echo "  Management Tools Analysis Dashboard"
echo "  Phase 5: Production Deployment"
echo "=========================================="
echo "📍 Dashboard URL: http://localhost:8050/"
echo "💾 Database: $(ls -la data/*.db 2>/dev/null || echo 'Not found')"
echo "🖼️  Assets: $(ls -la assets/ | wc -l) files"
echo "📊 Logs: $(ls -la logs/ 2>/dev/null || echo 'Directory created')"
echo "🔧 Environment: $(python --version 2>/dev/null || echo 'Python not available')"
echo "⏰ Started at: $(date)"
echo "=========================================="
echo ""

# Start the application
echo "🎯 Launching dashboard application..."
exec "$@"