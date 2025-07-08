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

### Technical Infrastructure
- FastAPI web application with health monitoring
- Celery background task processing
- PostgreSQL database with external access
- Redis message broker
- Flower task monitoring dashboard
- Auto-configuration based on project name suffix

### Project Management Framework
- Complete IADPVEC methodology for systematic development
- Knowledge preservation through commit statements and project status
- Task management system with prioritization and tracking
- Workflow documentation for standardized processes
- Session context preservation for seamless development

## Service Access

After installation, services available at:
- API: http://localhost:81XX (where XX = your suffix)
- Database: localhost:54XX
- Monitoring: http://localhost:55XX
- DB Admin: http://localhost:80XX

## Development Workflow

The template includes a comprehensive project management framework in the `project/` directory:

### Key Components
- **Architecture Documentation**: `project/PLANNING.md`
- **Current Sprint**: `project/TASK.md`
- **Project Goals**: `project/VISION.md`
- **AI Collaboration**: `project/CLAUDE.md`
- **Task Management**: `project/tasks/master_TASK_list.md`
- **Development Workflows**: `project/workflows/`

### Using the Framework
1. **Start Development**: Read `project/PLANNING.md` and `project/TASK.md`
2. **Follow IADPVEC**: Use the systematic workflow for all development
3. **Preserve Knowledge**: Create project status updates for all sessions
4. **Document Changes**: Use prepared commit statements for all changes
5. **Track Progress**: Update task status in `project/tasks/`

For more details, see `PROJECT_FOLDER_USAGE_GUIDE.md`.

Ready-to-use microservice foundation with automatic configuration and comprehensive project management.