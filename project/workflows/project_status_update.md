# Project Status Update Workflow

**Capture current project state in timestamped files within `project_status/` directory for session recovery, team collaboration, and framework portability.**

---

## 📁 **Project Status Directory Structure**

### **Directory Organization**
```
project/project_status/
├── 2025-07-04_06-15-23.txt    # Morning infrastructure discussion
├── 2025-07-04_08-45-17.txt    # Docker testing completed
├── 2025-07-04_10-30-41.txt    # Workflow documentation session
├── 2025-07-04_14-22-05.txt    # FastAPI development started
└── 2025-07-04_16-18-33.txt    # End of day status
```

### **Filename Convention**
- **Format:** `YYYY-MM-DD_HH-MM-SS.txt`
- **Example:** `2025-07-04_06-45-15.txt`
- **Timezone:** Local time (consistent with development environment)
- **Sorting:** Chronological order when listed alphabetically

### **File Content Standard**
```
=== PROJECT STATUS UPDATE ===
Created: [Full timestamp with timezone]
File: [Filename for reference]

RECENT COMMITS:
[Git log output]

CURRENT STATUS:
[Current state description]

[Context-specific sections]

BRANCH INFO:
[Git branch and commit info]
```

---

## 🔍 **Reading Project Status History**

### **AI Assistant Context Loading**

**Read recent updates:**
```bash
# Read last 5 status updates
ls project/project_status/*.txt | tail -5 | xargs cat

# Read last 10 status updates  
ls project/project_status/*.txt | tail -10 | xargs cat

# Read today's status updates
ls project/project_status/$(date +%Y-%m-%d)_*.txt | xargs cat

# Read specific time range
ls project/project_status/2025-07-04_*.txt | xargs cat
```

**Context management:**
- **Last 3 updates** → Quick recent context (~2000 tokens)
- **Last 5 updates** → Session context (~4000 tokens)  
- **Last 10 updates** → Full day context (~8000 tokens)
- **Specific date** → Complete day's progression

### **Session Recovery Commands**

**For AI assistants resuming work:**
```bash
# Quick context (most recent)
echo "Recent project status:"
cat $(ls project/project_status/*.txt | tail -1)

# Session context (last few updates)
echo "Session progression:"
ls project/project_status/*.txt | tail -3 | xargs -I {} sh -c 'echo "=== {} ==="; cat "{}"'

# Full day context
echo "Today's progress:"
ls project/project_status/$(date +%Y-%m-%d)_*.txt | xargs -I {} sh -c 'echo "=== {} ==="; cat "{}"'
```

## 🎯 **When to Use This Workflow**

### **Standalone Status Updates (No Code Changes)**
- Long conversations about planning or architecture
- IADPVEC phase discussions (DISCUSS, ASSESS phases)
- Session interruption points ("capture where we are")
- Research findings or decisions made
- Problem analysis or troubleshooting discoveries

### **Integrated with Code Commits**
- Called automatically from git commit workflow
- Ensures commit message data is also captured in project status
- Maintains consistent project state documentation

---

## 📋 **The Status Update Process**

### **Step 1: Create Project Status Directory**
Ensure the directory exists (only needed once per project):

```bash
mkdir -p project_status
```

### **Step 2: Generate Timestamped Status File**
Create individual status file with current timestamp:

```bash
# Generate filename with current timestamp
STATUS_FILE="project/project_status/$(date +%Y-%m-%d_%H-%M-%S).txt"

# Create status update
cat > "$STATUS_FILE" << 'EOF'
=== PROJECT STATUS UPDATE ===
Created: $(date)
File: $STATUS_FILE

RECENT COMMITS:
[Last 3-5 commit summaries from git log --oneline -5]

CURRENT STATUS:
[What just happened / current state]

[Optional sections based on context:]
DISCUSSION SUMMARY:
[Key points from conversations]

DECISIONS MADE:
[Architecture or implementation decisions]

NEXT STEPS:
[What should happen next]

BRANCH INFO:
Current branch: $(git branch --show-current)
Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)')
EOF
```

### **Step 3: Verify File Created**
```bash
echo "Status update saved to: $STATUS_FILE"
ls -la project/project_status/ | tail -5  # Show recent status files
```

---

## 🔄 **Template Examples**

### **Conversation Capture Template**
```bash
STATUS_FILE="project_status/$(date +%Y-%m-%d_%H-%M-%S).txt"
cat > "$STATUS_FILE" << 'EOF'
=== PROJECT STATUS UPDATE ===
Created: $(date)
File: $STATUS_FILE

RECENT COMMITS:
efa461c Fix git commit script to prevent vim editor
49d45f6 Initial project setup

CURRENT STATUS:
Long discussion about workflow documentation integration

DISCUSSION SUMMARY:
- Clarified need for separate commit vs status update workflows
- Established text expansion triggers for different procedures
- Designed integrated approach: commit workflow calls status workflow
- Status workflow can also run independently for conversations

DECISIONS MADE:
- Create two separate workflow documents with cross-references
- Git commit workflow includes status update step at end
- Text expansions will trigger appropriate procedure
- Use project_status/ directory instead of .git/ for portability

NEXT STEPS:
- Complete workflow documentation creation
- Test text expansion integration
- Begin FastAPI application development

BRANCH INFO:
Current branch: $(git branch --show-current)
Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)')
EOF
echo "Status saved to: $STATUS_FILE"
```

### **Research/Analysis Template**
```bash
STATUS_FILE="project_status/$(date +%Y-%m-%d_%H-%M-%S).txt"
cat > "$STATUS_FILE" << 'EOF'
=== PROJECT STATUS UPDATE ===
Created: $(date)
File: $STATUS_FILE

RECENT COMMITS:
$(git log --oneline -3)

CURRENT STATUS:
Infrastructure analysis and port testing completed

ANALYSIS RESULTS:
- All Docker services starting correctly
- Port strategy validated: 8101, 5401, 5501, 8001 working
- PostgreSQL external access confirmed
- Adminer web interface functional

ISSUES DISCOVERED:
- Celery services restarting (expected - missing app structure)
- FastAPI returns connection reset (expected - placeholder code)
- Database rcfpgapi_dev not created (needs initialization)

NEXT STEPS:
- Document infrastructure test results in PLANNING.md
- Create FastAPI application structure
- Initialize database with proper schema

BRANCH INFO:
Current branch: $(git branch --show-current)
Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)')
EOF
echo "Status saved to: $STATUS_FILE"
```

### **Decision Point Template**
```bash
STATUS_FILE="project_status/$(date +%Y-%m-%d_%H-%M-%S).txt"
cat > "$STATUS_FILE" << 'EOF'
=== PROJECT STATUS UPDATE ===
Created: $(date)
File: $STATUS_FILE

RECENT COMMITS:
$(git log --oneline -3)

CURRENT STATUS:
Architecture decision point reached for [topic]

OPTIONS DISCUSSED:
Option A: [Description and pros/cons]
Option B: [Description and pros/cons]
Option C: [Description and pros/cons]

DECISION MADE:
Chose Option [X] because [reasoning]

IMPLEMENTATION PLAN:
1. [Step one]
2. [Step two]
3. [Step three]

NEXT STEPS:
Begin implementation of decided approach

BRANCH INFO:
Current branch: $(git branch --show-current)
Last commit: $(git log -1 --pretty=format:'%h - %s (%cr)')
EOF
echo "Status saved to: $STATUS_FILE"
```

---

## 🛠️ **Advanced Usage**

### **Quick Status Updates**
For brief updates, use a simplified format:

```bash
STATUS_FILE="project_status/$(date +%Y-%m-%d_%H-%M-%S).txt"
echo "=== PROJECT STATUS UPDATE ===
Created: $(date)
File: $STATUS_FILE

CURRENT STATUS:
[Brief description of current state]

NEXT STEPS:
[What's happening next]" > "$STATUS_FILE"
echo "Quick status saved to: $STATUS_FILE"
```

### **IADPVEC Phase Tracking**
Include current IADPVEC phase in status:

```bash
STATUS_FILE="project_status/$(date +%Y-%m-%d_%H-%M-%S).txt"
cat > "$STATUS_FILE" << 'EOF'
=== PROJECT STATUS UPDATE ===
Created: $(date)
File: $STATUS_FILE

CURRENT STATUS:
[Description]

IADPVEC PHASE: DISCUSS
- Presented infrastructure testing approach
- Waiting for approval to proceed to PLAN phase

NEXT STEPS:
- Get explicit approval for testing methodology
- Move to PLAN phase if approved
EOF
echo "IADPVEC status saved to: $STATUS_FILE"
```

### **Batch Status Reading**
Read multiple status files for comprehensive context:

```bash
# Read last session (last 3 files)
echo "=== RECENT SESSION CONTEXT ==="
ls project_status/*.txt | tail -3 | while read file; do
    echo "\n--- $(basename "$file") ---"
    cat "$file"
done

# Read specific day's progression
DATE=$(date +%Y-%m-%d)
echo "=== TODAY'S PROGRESSION ($DATE) ==="
ls project_status/${DATE}_*.txt | while read file; do
    echo "\n--- $(basename "$file") ---"
    cat "$file"
done
```

---

## 🔧 **Integration Points**

### **Called from Git Commit Workflow**
When the git commit workflow completes, it references this document:

**"After committing, update project status using workflows/project_status_update.md"**

The status file will be created in `project_status/` and **included in the next commit** as part of project documentation.

### **Standalone Usage**
Use directly when:
- No code changes but important conversations happened
- Research or analysis completed
- Decisions made that affect future work
- Session ending points for recovery

### **Text Expansion Triggers**
Set up text expansions:
- **Trigger:** `;;status` 
- **Expansion:** "Follow workflows/project_status_update.md to capture current project state"

### **Framework Portability**
The `project_status/` directory:
- ✅ **Gets pushed to remote repositories** (unlike .git/ contents)
- ✅ **Travels with the framework** when cloned to new projects
- ✅ **Provides team visibility** into project progression
- ✅ **Preserves project history** across different development environments

---

## 📝 **Best Practices**

### **Status Content Guidelines**
- **Be specific** - Include concrete details, not vague summaries
- **Include context** - Help future you understand what was happening
- **Note decisions** - Capture reasoning behind choices made
- **Identify next steps** - Clear direction for resuming work

### **Update Frequency**
- **After significant conversations** - Planning, architecture discussions
- **At decision points** - When choices are made that affect direction
- **Before session ends** - Capture current state for recovery
- **When research completed** - Document findings and implications

### **Recovery Information**
Include enough detail that someone (including future you) can:
- Understand current project state
- Know what was last accomplished
- Identify what should happen next
- Resume work without losing context

---

## 🚀 **Integration with Project Framework**

### **AI Assistant Context**
When AI assistants read project status files, they get:
- Current project state and recent progress
- Decisions made and reasoning
- Next steps and priorities  
- Session context for seamless continuation

**Context loading examples:**
```bash
# Quick recent context (last status file)
cat $(ls project_status/*.txt | tail -1)

# Session context (last 5 status files)
ls project_status/*.txt | tail -5 | xargs cat

# Full day context (today's files)
ls project_status/$(date +%Y-%m-%d)_*.txt | xargs cat
```

### **Team Collaboration**
Status files provide:
- Project progress visibility across team members
- Decision history and rationale accessible to all
- Current focus areas for coordination
- Handoff information between developers
- Searchable project knowledge base

### **Project Documentation**
Status files become:
- Project history timeline with granular detail
- Decision audit trail with full context
- Progress tracking mechanism with timestamps
- Recovery documentation system for any point in time
- Framework knowledge base for future projects

---

**This workflow ensures consistent project state capture whether used standalone for conversations or integrated with code commits, enabling seamless project continuity and effective collaboration.**