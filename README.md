# Microservice Template Framework

**Auto-configurable microservice foundation with FastAPI + Celery + PostgreSQL + Redis**

## Quick Start

Clone template for your project:
```bash
git clone https://github.com/azure-architect/microservice-dev my-project-03
cd my-project-03

# Auto-configure with project suffix
python install.py

# Deploy immediately
docker-compose up -d
```

## What You Get

- FastAPI web application with health monitoring
- Celery background task processing
- PostgreSQL database with external access
- Redis message broker
- Flower task monitoring dashboard
- Auto-configuration based on project name

## Service Access

After installation, services available at:
- API: http://localhost:81XX (where XX = your suffix)
- Database: localhost:54XX
- Monitoring: http://localhost:55XX
- DB Admin: http://localhost:80XX

Ready-to-use microservice foundation with automatic configuration.
