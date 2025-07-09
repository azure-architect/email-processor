I'll create comprehensive setup and usage documentation for the microservice template repository.

## **PLAN: Complete Documentation Structure**

I'll create:
1. **Enhanced README.md** - Main entry point with quick start
2. **docs/INSTALLATION.md** - Detailed installation guide
3. **docs/USAGE.md** - Complete usage instructions
4. **docs/CUSTOMIZATION.md** - How to customize for specific needs
5. **docs/TROUBLESHOOTING.md** - Common issues and solutions
6. **docs/ARCHITECTURE.md** - Technical architecture details

**Step 1: Create docs directory**
```bash
mkdir -p docs
```

**Step 2: Create enhanced README.md**
```bash
cat > README.md << 'EOF'
# Microservice Template Framework

**Production-ready microservice foundation with auto-configuration**

A complete FastAPI + Celery + PostgreSQL + Redis microservice template that automatically configures ports, container names, and networking based on your project name.

## 🚀 Quick Start

```bash
# 1. Clone for your project (replace XX with 2-digit suffix)
git clone https://github.com/azure-architect/microservice-dev my-service-03
cd my-service-03

# 2. Auto-configure (detects suffix "03" from folder name)
python install.py

# 3. Activate virtual environment
source venv/bin/activate

# 4. Start all services
docker-compose up -d

# 5. Test your microservice
curl http://localhost:8103/health
```

**Your microservice is now running with:**
- 🌐 **API**: http://localhost:8103
- 🗄️ **Database**: localhost:5403  
- 📊 **Monitoring**: http://localhost:5503
- 🛠️ **DB Admin**: http://localhost:8003

## ✨ Features

### 🔄 **Auto-Configuration**
- **Smart port detection** - Suffix "03" → ports 8103, 5403, 5503, 8003
- **Project-specific naming** - Containers named `my-service-03-fastapi-03`
- **Network isolation** - Each project gets isolated Docker network
- **Environment generation** - Automatic .env file with correct settings

### 🏗️ **Complete Infrastructure**
- **FastAPI** - Modern async web framework with automatic docs
- **Celery** - Background task processing with Redis broker
- **PostgreSQL** - Production database with external access
- **Redis** - Fast in-memory data store and message broker
- **Flower** - Real-time Celery task monitoring
- **Docker** - Complete containerized deployment

### 🛠️ **Developer Experience**
- **Virtual environment** - Clean dependency isolation
- **Health monitoring** - Built-in health checks and status endpoints
- **Template files** - Examples for common patterns
- **Hot reload** - Development-friendly configuration
- **Comprehensive testing** - Ready-to-use test structure

## 📖 Documentation

| Guide | Description |
|-------|-------------|
| [Installation](docs/INSTALLATION.md) | Detailed setup instructions |
| [Usage](docs/USAGE.md) | Complete usage guide |
| [Customization](docs/CUSTOMIZATION.md) | How to adapt for your needs |
| [Architecture](docs/ARCHITECTURE.md) | Technical details |
| [Troubleshooting](docs/TROUBLESHOOTING.md) | Common issues & solutions |

## 🎯 Use Cases

### Perfect For:
- **Microservice APIs** - RESTful services with background processing
- **Data processors** - ETL pipelines with task queues
- **Async workflows** - Event-driven architectures
- **Prototype APIs** - Rapid development with production patterns
- **Learning projects** - Modern Python web development

### Multiple Projects:
```bash
# Clone multiple projects with different suffixes
git clone ... data-processor-01    # → ports 8101, 5401, 5501, 8001
git clone ... user-service-02      # → ports 8102, 5402, 5502, 8002  
git clone ... file-handler-03      # → ports 8103, 5403, 5503, 8003
```

## 📁 Project Structure

```
my-service-03/
├── src/                           # Application source code
│   ├── api/                       # FastAPI routes and endpoints  
│   │   └── routes/
│   │       ├── health.py          # Health check endpoints
│   │       └── ...                # Your custom routes
│   ├── workers/                   # Celery background tasks
│   │   ├── celery_app.py          # Celery configuration
│   │   └── tasks/
│   │       ├── health_tasks.py    # Essential health tasks
│   │       └── ...                # Your custom tasks
│   ├── core/                      # Core configuration
│   └── models/                    # Data models and schemas
├── tests/                         # Test suite
├── templates/                     # Code templates for customization
├── docker-compose.yml             # Generated service configuration
├── .env                          # Generated environment variables
├── Dockerfile                    # Container build configuration
├── requirements.txt              # Python dependencies
└── install.py                   # Auto-configuration script
```

## ⚡ Quick Examples

### Add a New API Endpoint
```python
# src/api/routes/users.py
from fastapi import APIRouter

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/{user_id}")
async def get_user(user_id: int):
    return {"user_id": user_id, "name": "John Doe"}
```

### Add a Background Task
```python
# src/workers/tasks/user_tasks.py
from ..celery_app import celery_app

@celery_app.task
def send_welcome_email(user_id: int):
    # Your email logic here
    return {"status": "sent", "user_id": user_id}
```

### Test Your Code
```python
# tests/api/test_users.py
def test_get_user(client):
    response = client.get("/users/123")
    assert response.status_code == 200
    assert response.json()["user_id"] == 123
```

## 🔧 Development Workflow

```bash
# 1. Clone and configure
git clone https://github.com/azure-architect/microservice-dev my-app-05
cd my-app-05
python install.py

# 2. Start development environment
source venv/bin/activate
docker-compose up -d

# 3. Develop your application
# - Add routes in src/api/routes/
# - Add tasks in src/workers/tasks/  
# - Add tests in tests/

# 4. Test your changes
pytest tests/ -v
curl http://localhost:8105/health

# 5. Monitor background tasks
open http://localhost:5505  # Flower dashboard
```

## 🌟 Why This Template?

### vs Starting from Scratch
- ✅ **Save weeks of setup** - Complete infrastructure ready
- ✅ **Production patterns** - Best practices built-in
- ✅ **No configuration conflicts** - Auto-managed ports and naming

### vs Other Templates  
- ✅ **Auto-configuration** - No manual port management
- ✅ **Multi-project support** - Run many microservices simultaneously
- ✅ **Complete stack** - Database, cache, monitoring included
- ✅ **Modern tools** - FastAPI, Celery, PostgreSQL, Redis

## 🆘 Need Help?

- 📚 **[Complete Documentation](docs/)** - Detailed guides
- 🐛 **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues
- 💡 **[Examples](templates/)** - Code templates and patterns
- 🔧 **[Architecture](docs/ARCHITECTURE.md)** - Technical details

## 📄 License

MIT License - Feel free to use for any project!

---

**Ready to build your microservice? Get started in 2 minutes!** 🚀

```bash
git clone https://github.com/azure-architect/microservice-dev my-project-XX
cd my-project-XX && python install.py && source venv/bin/activate && docker-compose up -d
```
EOF
```

**Run these commands and let me know when complete.**