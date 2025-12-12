# Docker Deployment Guide - Management Tools Analysis Dashboard

**Phase 5: Production Deployment & Monitoring**

## Quick Start

### Development
```bash
# Build and run development version
cd dashboard_app
docker-compose up --build

# Or with development profile (hot reload)
docker-compose --profile development up --build
```

### Production
```bash
# Build and run production version
cd dashboard_app
docker-compose up --build -d

# View logs
docker-compose logs -f dashboard

# Stop services
docker-compose down
```

## Docker Files Created

### 📄 Dockerfile
- **Location**: `dashboard_app/Dockerfile`
- **Purpose**: Main container image for the dashboard
- **Features**:
  - Python 3.11 slim base image
  - uv package manager for fast dependency installation
  - Non-root user for security
  - Health checks included
  - Optimized for production

### 📄 docker-compose.yml
- **Location**: `dashboard_app/docker-compose.yml`
- **Purpose**: Orchestrate development and production services
- **Services**:
  - `dashboard`: Main application service
  - `monitoring`: Optional Prometheus monitoring (profile: monitoring)
  - `nginx`: Optional reverse proxy (profile: production)

### 📄 .dockerignore
- **Location**: `dashboard_app/.dockerignore`
- **Purpose**: Exclude unnecessary files from Docker build
- **Benefits**: Faster builds, smaller images

### 📄 docker/entrypoint.sh
- **Location**: `dashboard_app/docker/entrypoint.sh`
- **Purpose**: Container startup script
- **Features**:
  - Environment validation
  - Database wait logic
  - Graceful shutdown handling
  - Startup logging

## Environment Configuration

### Required Environment Variables
Create a `.env` file in the `dashboard_app` directory:

```bash
# Copy from template
cp .env.example .env

# Edit .env with your configuration
nano .env
```

### Key Variables
```bash
# API Keys (required)
GROQ_API_KEY=your_groq_api_key_here
OPENROUTER_API_KEY=your_openrouter_api_key_here

# Database Configuration
DATABASE_URL=sqlite:///data/precomputed_findings.db

# Application Settings
FLASK_ENV=production
DASH_DEBUG=false
PORT=8050

# Security
SECRET_KEY=your_secret_key_here
REGENERATION_API_SECRET=your_regeneration_secret_key
```

## Deployment Profiles

### Development Profile
```bash
# Enable hot reload and development tools
docker-compose --profile development up --build

# Features:
# - Source code mounted for hot reload
# - Debug mode enabled
# - Development database (optional)
```

### Monitoring Profile
```bash
# Enable Prometheus monitoring
docker-compose --profile monitoring up -d

# Access:
# - Dashboard: http://localhost:8050
# - Prometheus: http://localhost:9090
```

### Production Profile
```bash
# Enable production reverse proxy
docker-compose --profile production up -d

# Features:
# - Nginx reverse proxy
# - SSL/TLS support
# - Production optimizations
```

## Volume Mounts

### Data Persistence
- `../data:/app/data` - Database files and cached data
- `../logs:/app/logs` - Application logs
- `./assets:/app/assets` - Static assets (images, etc.)

### Development Mounts
- `.:/app` - Source code (development only)
- Hot reload enabled for real-time development

## Health Checks

### Built-in Health Check
```bash
# Docker health check
docker-compose ps

# Manual health check
curl -f http://localhost:8050/
```

### Custom Health Endpoint
```bash
# Check container health
docker inspect --format='{{.State.Health.Status}}' management-tools-dashboard
```

## Troubleshooting

### Common Issues

#### Container won't start
```bash
# Check logs
docker-compose logs dashboard

# Verify environment
docker-compose config
```

#### Database not accessible
```bash
# Check volume mounts
docker-compose exec dashboard ls -la /app/data

# Verify database file
docker-compose exec dashboard ls -la /app/data/*.db
```

#### Port already in use
```bash
# Change port in docker-compose.yml
ports:
  - "8051:8050"  # Use different external port
```

### Performance Issues

#### Slow startup
```bash
# Check Docker build cache
docker system prune -a

# Rebuild without cache
docker-compose build --no-cache
```

#### Memory issues
```bash
# Check container resources
docker stats

# Limit memory usage
deploy:
  resources:
    limits:
      memory: 1G
```

## Next Steps

Phase 5.1 (Docker containerization) is now complete! 🚀

**Next Phase 5 Tasks**:
- [ ] Implement CI/CD pipeline with automated testing
- [ ] Add production monitoring and alerting system
- [ ] Create backup and disaster recovery procedures
- [ ] Implement comprehensive load testing suite

## Useful Commands

```bash
# Quick start
docker-compose up --build -d

# View logs
docker-compose logs -f dashboard

# Restart services
docker-compose restart dashboard

# Update and redeploy
docker-compose pull && docker-compose up -d

# Clean shutdown
docker-compose down --volumes --remove-orphans
```