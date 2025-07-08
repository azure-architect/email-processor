# Project Architecture & Planning

## 🎯 Project Overview

### Purpose
**What this project does:** A production-ready microservice template that auto-configures itself based on the project folder name suffix, enabling multiple microservices to run simultaneously without port conflicts.

### Business Value

**Problem it solves:** Eliminates the friction and configuration errors when setting up new microservices by automatically handling port assignments, container naming, and network isolation.

**Target users:**
- Development teams building microservice architectures
- Individual developers creating multiple related services
- DevOps engineers setting up deployment pipelines
- Students and learners exploring microservice development

**Success metrics:**
- Setup time reduction: <2 minutes from clone to operational service
- Configuration errors: Zero port conflicts across multiple deployments
- Developer experience: Intuitive, well-documented workflows
- Template versatility: Successfully used across multiple project types
- Adoption rate: Number of projects using this template

## 🏗️ System Architecture

### High-Level Design
```
Microservice Template Architecture:
- Auto-Configuration Layer: Project suffix detection and environment setup
- Web API Layer: FastAPI with health monitoring endpoints
- Background Processing: Celery tasks with Redis broker
- Data Persistence: PostgreSQL with external access 
- Monitoring: Flower dashboard for task visualization
- Development Tools: Adminer web interface for database management
```

### Key Technologies
- **Primary Language:** Python 3.12+
- **Framework:** FastAPI (async API framework)
- **Database:** PostgreSQL (with external port access)
- **Background Processing:** Celery with Redis
- **Infrastructure:** Docker containerization
- **Testing:** Pytest with async support
- **Project Management:** IADPVEC methodology framework

### External Dependencies
- **Services:** PostgreSQL, Redis, Adminer
- **Libraries:** 
  - `fastapi` (API framework)
  - `sqlalchemy` (database ORM with async support)
  - `celery` (distributed task processing)
  - `pydantic` (data validation and serialization)
  - `httpx` (async HTTP client for API calls)

### Port Strategy
The auto-configuration system uses the 2-digit suffix from the project folder name to assign unique ports:
- **FastAPI:** 81XX (e.g., 8101)
- **PostgreSQL:** 54XX (e.g., 5401)
- **Flower:** 55XX (e.g., 5501)
- **Adminer:** 80XX (e.g., 8001)

## 📁 Code Organization

### Module Structure
```
project-root/
├── src/                    # Main application code
│   ├── api/                # API endpoints and routing
│   │   └── routes/         # API route modules
│   ├── core/               # Core business logic
│   │   └── config.py       # Configuration settings
│   ├── models/             # Data models and schemas
│   │   └── database.py     # Database connection
│   └── workers/            # Background tasks
│       ├── celery_app.py   # Celery configuration
│       └── tasks/          # Task modules
├── project/                # Project management framework
│   ├── commit_statements/  # Git commit documentation
│   ├── project_status/     # Session state tracking
│   ├── workflows/          # Development processes
│   ├── tasks/              # Task management
│   └── PLANNING.md         # Architecture documentation
├── tests/                  # Test suite
├── docker-compose.yml      # Container orchestration
├── Dockerfile              # Container definition
├── install.py              # Auto-configuration script
└── requirements.txt        # Python dependencies
```

### Design Patterns
- **Dependency Injection:** FastAPI's dependency system manages database connections, configuration, and services
- **Repository Pattern:** Abstracts data access operations from business logic
- **Factory Pattern:** Configuration factory creates application settings from environment
- **Auto-Configuration:** Suffix detection dynamically configures ports and containers

### Naming Conventions
- **Files:** snake_case for Python, kebab-case for configs
- **Classes:** PascalCase
- **Functions/Variables:** snake_case
- **Constants:** UPPER_SNAKE_CASE
- **APIs:** RESTful conventions with clear resource naming

## 🔧 Development Standards

### Code Quality
- **Line Length:** 88 characters (Black default)
- **Type Hints:** Required for all public functions
- **Docstrings:** Google style for all public functions/classes
- **Linting:** Ruff for linting, Black for formatting
- **Type Checking:** MyPy with strict mode

### Testing Strategy
- **Unit Tests:** 80%+ coverage for core business logic
- **Integration Tests:** API endpoints and database interactions
- **End-to-End Tests:** Critical user workflows
- **Test Naming:** test_should_[expected_behavior]_when_[condition]

### Git Workflow
- **Branching:** Feature branches from main with IADPVEC task validation
- **Commits:** Timestamped commit statement files in project/commit_statements/
- **Project Status:** Matching timestamped status updates in project/project_status/
- **Documentation:** Complete workflow integration following project/workflows/ procedures
- **Releases:** Semantic versioning with comprehensive commit and status history

### Quality Gates
```bash
# Pre-commit checks
ruff check . --fix              # Linting and auto-fixes
black .                         # Code formatting
mypy .                          # Type checking
pytest tests/ -v --cov=src      # Test suite with coverage

# CI/CD pipeline requirements
- All tests pass
- Coverage >= 80%
- No type errors
- No security vulnerabilities
- Documentation updated
```

## 🚦 Development Workflow

### IADPVEC Integration
- **INGEST:** Always read this PLANNING.md first
- **ASSESS:** Evaluate against these architectural principles
- **DISCUSS:** Reference these patterns in solution proposals
- **PLAN:** Follow these organizational structures
- **VALIDATE:** Use these quality gates
- **EXECUTE:** Only after explicit approval
- **COMMIT:** Document architectural decisions

### Feature Development Process
1. **Context Gathering:** Read PLANNING.md, TASK.md, relevant examples
2. **Architecture Review:** Ensure feature fits system design
3. **Implementation Planning:** Create detailed technical plan
4. **Quality Validation:** Meet all quality gates
5. **Documentation:** Update relevant docs and examples

## 🔒 Security & Compliance

### Security Requirements
- **Authentication:** JWT-based when needed
- **Authorization:** Role-based permission system
- **Data Protection:** Environment-based configuration with .env files
- **API Security:** Rate limiting, input validation, proper error handling

### Compliance Considerations
- **Data Privacy:** No PII in logs, configurable data retention
- **Audit Trail:** Comprehensive logging with correlation IDs
- **Backup Strategy:** Database volume mapping for persistence
- **Error Handling:** Structured error responses with appropriate status codes

## 🚀 Deployment & Operations

### Environment Strategy
- **Development:** Local development with Docker
- **Staging:** Configurable via environment variables
- **Production:** Production-ready with proper settings

### Monitoring & Observability
- **Logging:** Structured logging with correlation IDs
- **Metrics:** Health endpoint with service status
- **Alerting:** Configurable based on health status
- **Health Checks:** `/health` endpoint for Docker and orchestration

## 📚 Documentation Standards

### Code Documentation
- **README:** Setup, usage, and deployment instructions
- **API Docs:** OpenAPI/Swagger for all endpoints
- **Architecture Docs:** PLANNING.md with technical decisions
- **Workflows:** Detailed workflow documentation in project/workflows/

### Knowledge Management
- **Decision Records:** Commit statements with rationale
- **Session Context:** Project status files with discussions
- **Examples:** Working code examples for common patterns
- **Troubleshooting:** Common issues and solutions

---

## 🎯 Success Criteria

### Technical Criteria
- [ ] Auto-configuration works across multiple project deployments
- [ ] All services start and communicate properly
- [ ] Health monitoring provides accurate service status
- [ ] Background tasks execute reliably
- [ ] Documentation comprehensive and accurate

### Process Criteria
- [ ] IADPVEC methodology framework fully implemented
- [ ] Project management tools (commit statements, status updates) operational
- [ ] Setup time under 2 minutes from clone to running
- [ ] Multiple instances can run simultaneously without conflicts
- [ ] Developers can quickly understand and extend the template

---

*This PLANNING.md serves as the architectural source of truth. Update it when making significant architectural decisions, and always reference it during IADPVEC workflows.*

**Last Updated:** 2025-07-08 - Added project management framework based on youtube-kb-04 project