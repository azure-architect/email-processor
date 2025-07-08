# Git Workflow: Commit with Timestamped Files

**Integrated workflow for committing changes using timestamped commit statement files and automatic project status updates.**

---

## 🔄 **Complete Integrated Workflow**

### **Automated Process: Commit + Status Update**

**This workflow creates BOTH a commit statement AND project status update with matching timestamps, then provides the exact git command to execute.**

👉 **Calls:** `project/workflows/project_status_update.md` automatically

**Why both are needed:**
- **Commit statement** → Detailed commit message for git history
- **Project status** → Broader session context and decisions
- **Matching timestamps** → Easy correlation between commit and status
- **Complete archival** → All project knowledge preserved and portable

### **The Integrated Process:**
```bash
# 1. AI creates timestamped commit statement
project/commit_statements/YYYY-MM-DD_HH-MM-SS.txt

# 2. AI creates matching project status update
project/project_status/YYYY-MM-DD_HH-MM-SS.txt

# 3. AI provides exact git command
git add [relevant files]
git commit -F project/commit_statements/YYYY-MM-DD_HH-MM-SS.txt
```

### **Text Expansion Integration**

**For code commits with status:**
- **Trigger:** `;;commit`
- **Action:** "Follow workflows/git_commit_with_prepared_message.md to capture code changes and project state"

**For status-only updates:**
- **Trigger:** `;;status`  
- **Action:** "Follow workflows/project_status_update.md to capture current project state"

---

## 📁 **Directory Structure**

### **Commit Statements Archive**
```
project/commit_statements/
├── 2025-07-04_06-15-23.txt    # Infrastructure validation commit
├── 2025-07-04_08-45-17.txt    # Docker testing completion
├── 2025-07-04_10-30-41.txt    # Workflow documentation
├── 2025-07-04_14-22-05.txt    # FastAPI development
└── 2025-07-04_16-18-33.txt    # End of day commit
```

### **Matching Project Status**
```
project/project_status/
├── 2025-07-04_06-15-23.txt    # Same timestamp
├── 2025-07-04_08-45-17.txt    # Same timestamp
├── 2025-07-04_10-30-41.txt    # Same timestamp
├── 2025-07-04_14-22-05.txt    # Same timestamp
└── 2025-07-04_16-18-33.txt    # Same timestamp
```

### **Filename Convention**
- **Format:** `YYYY-MM-DD_HH-MM-SS.txt`
- **Example:** `2025-07-04_07-15-42.txt`
- **Matching:** Commit statement and project status use identical timestamps
- **Sorting:** Chronological order when listed alphabetically

---

## 🎯 **When to Use This Workflow**

Use this integrated workflow when you have:
- **Code changes to commit** - New features, bug fixes, infrastructure updates
- **Documentation updates** - README, PLANNING.md, workflow documentation
- **Configuration changes** - Docker, environment, scripts
- **Project structure changes** - New directories, file organization
- **Any work that needs both git history AND session context**

**The workflow automatically handles:**
- ✅ **Timestamped commit statement creation**
- ✅ **Matching project status update**  
- ✅ **Exact git command generation**
- ✅ **Archive preservation for framework portability**

---

## 📋 **The Complete Workflow Process**

### **Step 1: AI Creates Commit Statement**
AI generates timestamped commit statement file:

```
commit_statements/YYYY-MM-DD_HH-MM-SS.txt
```

**Content structure:**
```
[Brief summary line]

- [Implementation detail 1]
- [Implementation detail 2] 
- [Test results or validation]

Technical details:
- [Performance metrics or configuration]
- [Dependencies or integrations]

Follows patterns from:
- [Reference documentation]

Resolves: [Task reference]
Files: [List of modified files]
Tests: [Test results]
```

### **Step 2: AI Creates Matching Project Status**
AI generates matching project status update:

```
project_status/YYYY-MM-DD_HH-MM-SS.txt
```

**Content includes broader context:**
- Session discussions and decisions
- IADPVEC phase tracking
- Next steps and priorities
- Architecture decisions made
- Issues discovered and resolved

### **Step 3: AI Provides Exact Git Command**
AI returns the specific command to execute:

```bash
git add [specific files that were changed]
git commit -F commit_statements/YYYY-MM-DD_HH-MM-SS.txt
```

**No guesswork needed** - exact filename and staging provided.

---

## 🔄 **Example Workflow Execution**

### **Complete Example: Infrastructure Validation Commit**

**AI Creates Commit Statement:**
```
project/commit_statements/2025-07-04_07-20-15.txt
```

**Content:**
```
Add workflow documentation system and infrastructure validation

- Created timestamped project status system in project_status/ directory
- Updated git commit workflow to use commit_statements/ archive
- Validated Docker infrastructure with all ports working correctly
- Established integrated ;;commit and ;;status text expansion triggers

Technical details:
- Port strategy confirmed: 8101, 5401, 5501, 8001 all accessible
- PostgreSQL external access validated
- Adminer web interface functional
- Framework portability achieved with version-controlled status files

Follows patterns from:
- workflows/project_status_update.md (timestamped file approach)
- workflows/git_commit_with_prepared_message.md (integrated workflow)

Resolves: Infrastructure validation and workflow documentation tasks
Files: workflows/, project_status/, commit_statements/, src/, tests/, PLANNING.md
Tests: Docker infrastructure validation passed, workflow system tested
```

**AI Creates Matching Project Status:**
```
project/project_status/2025-07-04_07-20-15.txt
```

**AI Provides Exact Command:**
```bash
git add workflows/ project_status/ commit_statements/ src/ tests/ PLANNING.md VIOLATIONS.md
git commit -F project/commit_statements/2025-07-04_07-20-15.txt
```

---

## ✅ **Benefits of This Integrated Approach**

### **Complete Knowledge Preservation**
- **Commit statements archived** - Complete commit history with detailed context
- **Project status archived** - Session context and decision history
- **Matching timestamps** - Easy correlation between commits and discussions
- **Framework portable** - All documentation travels with codebase

### **Workflow Efficiency**
- **No manual correlation** - AI creates both files simultaneously
- **Exact commands provided** - No guesswork on filenames or staging
- **Consistent formatting** - Standardized commit and status structure
- **Text expansion ready** - `;;commit` triggers complete workflow

### **Team Collaboration**
- **Visible commit history** - Team can see detailed commit reasoning
- **Shared context** - Project status updates visible to all
- **Knowledge transfer** - Complete context available when onboarding
- **Decision audit trail** - Why changes were made is preserved

### **AI Assistant Integration**
- **Context loading** - "Read last 5 commits" loads both statements and status
- **Session recovery** - Complete project state available for resumption
- **Pattern learning** - AI can reference previous similar work
- **Consistency enforcement** - Established patterns followed automatically

---

---

## 🔍 **Reading Commit and Status History**

### **Context Loading for AI Assistants**

**Read recent commits with context:**
```bash
# Last 3 commits with matching status
for file in $(ls commit_statements/*.txt | tail -3); do
    echo "=== COMMIT: $(basename $file) ==="
    cat "$file"
    echo "\n=== STATUS: $(basename $file) ==="
    cat "project_status/$(basename $file)"
    echo "\n---\n"
done

# Today's commits and status
DATE=$(date +%Y-%m-%d)
echo "=== TODAY'S COMMITS AND STATUS ($DATE) ==="
for file in commit_statements/${DATE}_*.txt; do
    if [ -f "$file" ]; then
        echo "\n--- COMMIT: $(basename $file) ---"
        cat "$file"
        echo "\n--- STATUS: $(basename $file) ---"
        cat "project_status/$(basename $file)"
    fi
done
```

### **Commit History Analysis**
```bash
# List all commits chronologically
ls commit_statements/*.txt

# Compare git log with commit statements
echo "=== GIT LOG ==="
git log --oneline -10
echo "\n=== COMMIT STATEMENTS ==="
ls commit_statements/*.txt | tail -10 | xargs -I {} basename {}

# Verify commit statement usage
git log --pretty=format:"%h %s" | head -5
```

---

**This integrated workflow ensures complete project knowledge preservation through timestamped commit statements and matching project status updates, providing exact git commands and maintaining framework portability across all development environments.**