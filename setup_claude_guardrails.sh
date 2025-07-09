#!/bin/bash
# Setup script for Claude guardrails

# Create .claude directory if it doesn't exist
mkdir -p .claude

# Create a minimal hooks.toml file with a notification hook
cat > .claude/hooks.toml << 'EOF'
# Basic notification hook that reminds Claude about guardrails
[[hooks]]
event = "Notification"
command = """
#!/bin/bash
echo "REMINDER: Follow the guardrails in CLAUDE.md"
echo "Always create scripts for the developer to review and run"
echo "Never execute commands that modify the codebase directly"
echo "Always check with the developer before proposing major changes"
"""
EOF

# Create an enhanced CLAUDE.md file with clearer guardrails
cat > project/CLAUDE.md << 'EOF'
# Claude Collaboration Guidelines

**Optimized framework for AI-assisted development with strict guardrails**

---

## 🛑 CRITICAL GUARDRAILS - READ FIRST

### Core Development Constraints
1. **NEVER execute commands that modify the codebase directly**
2. **ALWAYS create scripts for the developer to review and run**
3. **NEVER propose destructive operations without explicit warnings**
4. **ALWAYS get approval before implementing ANY changes**
5. **NEVER go in directions not explicitly approved by the developer**

### Safe Workflow Process
1. **Developer requests a task or change**
2. **Claude proposes a script to accomplish the task**
3. **Developer reviews the script and decides whether to run it**
4. **Developer executes the script if approved**
5. **Claude helps interpret results and suggests next steps**

### Examples of ACCEPTABLE Responses
- "Here's a script that would accomplish that task: [script details]"
- "I can help by creating a script that would: [description]"
- "Let me create a plan for implementing that change as a script"
- "I've written a script for your review that will make those changes safely"

### Examples of UNACCEPTABLE Responses
- Directly modifying files without developer review
- Running commands that change the repository state
- Making architectural decisions without explicit approval
- Adding new dependencies or systems without discussion

---

## 🎯 Collaboration Principles

### Core Development Philosophy
1. **Systematic Analysis** - Always start with thorough context understanding
2. **Explicit Approval** - Never implement without clear developer approval
3. **Complete Documentation** - Document all decisions and implementation details
4. **Framework Consistency** - Follow established patterns and architecture
5. **Knowledge Preservation** - Capture all context in project status files

### IADPVEC Adherence
- Follow the IADPVEC methodology for all significant development work:
  - **INGEST** - Read project files and understand context before proposing solutions
  - **ASSESS** - Analyze current state and requirements thoroughly
  - **DISCUSS** - Propose solutions with technical rationale
  - **PLAN** - Create detailed implementation plans
  - **VALIDATE** - Verify implementation against success criteria
  - **EXECUTE** - Implement solutions following approved plans
  - **COMMIT** - Document all changes with detailed context

---

## 📁 Critical Files to Read

### Always Reference These Files First
- **`project/PLANNING.md`** - Architecture and technical design
- **`project/TASK.md`** - Current sprint priorities and progress
- **`project/VISION.md`** - Project goals and success metrics
- **Most recent project status** - Latest in project/project_status/

### For Specific Tasks
- **Task file** - Detailed task requirements in project/tasks/
- **Relevant workflow file** - Process guidelines in project/workflows/
- **Related source files** - Understanding existing implementation

---

## 🔄 Session Workflow

### Session Start
1. **Load context from project status:**
   ```bash
   cat $(ls -t project/project_status/*.txt | head -1)
   ```
2. **Read current priorities:**
   ```bash
   grep -A 10 "## 🎯 Current Sprint" project/TASK.md
   ```
3. **Find active tasks:**
   ```bash
   grep -l "In Progress" project/tasks/*.md
   ```

### During Development
1. **Follow IADPVEC methodology phases explicitly**
2. **Reference project/PLANNING.md for architectural decisions**
3. **Use project status updates to capture discussions**
4. **Create and update task files with progress**

### Session End
1. **Create project status update:**
   ```bash
   # See project/workflows/project_status_update.md
   ```
2. **Prepare commit statement if implementation completed:**
   ```bash
   # See project/workflows/git_commit_with_prepared_message.md
   ```
3. **Update task status in project/TASK.md**

---

## 💬 Communication Guidelines

### Terminology
- Use consistent terminology from project/PLANNING.md
- Reference architecture components by their exact names
- Use microservice-specific terms properly (e.g., service, task, broker)

### Specificity
- Be specific about file paths and component names
- Prefer concrete examples over abstract explanations
- Reference existing code patterns when proposing new solutions

### Architectural Alignment
- Always align proposals with existing architecture
- Highlight deviations from established patterns explicitly
- Suggest improvements only with clear rationale

---

## 📝 Code Generation Guidelines

### Style and Standards
- **Line Length:** 88 characters (Black default)
- **Type Hints:** Required for all public functions
- **Docstrings:** Google style for all public functions/classes
- **Naming:** Follow project conventions (see PLANNING.md)
- **Error Handling:** Always include comprehensive error handling

### Pattern Adherence
- Follow dependency injection pattern using FastAPI dependencies
- Use repository pattern for data access logic
- Implement async patterns consistently for I/O operations
- Apply factory pattern for configuration management

### Testing Standards
- Include test coverage in implementation proposals
- Follow test naming convention: test_should_[expected_behavior]_when_[condition]
- Include both happy path and error case tests
- Use pytest fixtures for test setup

---

## 🚫 Development Constraints

### Never Violate These Rules
1. **No implementation without explicit approval**
2. **No architectural changes without discussion**
3. **No deviation from project structure**
4. **No partial implementations**
5. **No undocumented decisions**

### File Size Limits
- **Maximum file size:** 500 lines
- **Maximum function size:** 50 lines
- **Maximum class size:** 300 lines
- **Maximum module size:** 1000 lines

### Documentation Requirements
- All public functions must have docstrings
- All modules must have module-level docstrings
- All complex algorithms must have inline comments
- All configuration options must be documented

---

## 🧩 Implementation Patterns

### FastAPI Endpoints
```python
@router.get("/health", response_model=HealthResponse)
async def health_check(
    db: Database = Depends(get_db),
    redis: Redis = Depends(get_redis)
) -> HealthResponse:
    """Check service health status including dependencies.
    
    Returns comprehensive health information about the service
    and its dependencies (database, Redis, etc.)
    
    Args:
        db: Database connection from dependency injection
        redis: Redis connection from dependency injection
        
    Returns:
        HealthResponse: Health status information
    """
    try:
        db_status = await check_database_health(db)
        redis_status = await check_redis_health(redis)
        
        return HealthResponse(
            status="healthy" if db_status and redis_status else "degraded",
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=settings.app_version,
            database_status=db_status,
            redis_status=redis_status
        )
    except Exception as e:
        logger.error(f"Health check failed: {e}")
        return HealthResponse(
            status="unhealthy",
            timestamp=datetime.now(timezone.utc).isoformat(),
            version=settings.app_version,
            error=str(e)
        )
```

### Celery Tasks
```python
@celery_app.task(
    bind=True,
    name="process_data",
    max_retries=3,
    default_retry_delay=60
)
def process_data_task(self, data_id: int) -> Dict[str, Any]:
    """Process data asynchronously.
    
    Args:
        self: Task instance (bound task)
        data_id: ID of data to process
        
    Returns:
        Dict with processing results
        
    Raises:
        Retry: When temporary errors occur
        Exception: For critical errors
    """
    logger.info(f"Processing data: {data_id}")
    try:
        # Data processing logic
        result = {"status": "success", "data_id": data_id}
        return result
    except TemporaryError as e:
        logger.warning(f"Temporary error, retrying: {e}")
        raise self.retry(exc=e)
    except Exception as e:
        logger.error(f"Failed to process data {data_id}: {e}")
        raise
```

### SQLAlchemy Models
```python
class User(Base):
    """User model for authentication and profile information.
    
    Attributes:
        id: Unique user identifier
        username: Unique username for login
        email: User's email address
        hashed_password: Securely hashed password
        is_active: Whether user account is active
        created_at: When user was created
        updated_at: When user was last updated
    """
    __tablename__ = "users"
    
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = Column(String(50), unique=True, nullable=False, index=True)
    email = Column(String(100), unique=True, nullable=False)
    hashed_password = Column(String(100), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # Relationships
    profile = relationship("UserProfile", back_populates="user", uselist=False)
    
    def __repr__(self) -> str:
        return f"<User {self.username}>"
```

---

## 🛠️ Workflow Tools

### Task Management
- Create task files in project/tasks/ following templates
- Update project/TASK.md with current progress
- Use IADPVEC phases to track task progress

### Git Workflow
- Use project/workflows/git_commit_with_prepared_message.md
- Create timestamped commit statements
- Include matching project status updates

### Project Status
- Create status updates for all significant discussions
- Use project/workflows/project_status_update.md
- Include IADPVEC phase tracking

---

## 📈 Success Metrics for AI Collaboration

### Quality Metrics
- **Context completeness** - AI references all relevant project files
- **Architecture alignment** - Proposals match existing architecture
- **Documentation quality** - Complete and accurate documentation
- **Implementation completeness** - Full solutions, not partial work

### Process Metrics
- **IADPVEC adherence** - Follows methodology explicitly
- **Explicit permissions** - Seeks approval before implementation
- **Knowledge preservation** - Creates thorough project status updates
- **Commit quality** - Detailed commit statements with context

---

*These guidelines ensure consistent, high-quality AI-assisted development following proven methodologies. They establish clear expectations for all AI-human collaboration within this project.*

**Last Updated:** 2025-07-09 - Enhanced guardrails for safer collaboration
EOF

echo "Setup complete!"
echo "Created .claude/hooks.toml with notification hook"
echo "Created enhanced CLAUDE.md with clearer guardrails"
echo ""
echo "This setup establishes a safer workflow where:"
echo "1. Claude is reminded to follow guardrails"
echo "2. CLAUDE.md explicitly defines the script-first approach"
echo "3. The developer maintains full control over all changes"
