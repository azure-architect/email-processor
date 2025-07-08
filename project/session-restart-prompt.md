# Session Restart Prompt

**Use this prompt to provide quick context when resuming a development session with Claude.**

---

Hi Claude,

I'm resuming work on the microservices-01 project. Before we continue, please:

1. **Read the most recent project status update**:
   ```bash
   cat $(ls -t /Volumes/Samsung/mo/projects/research/proof-of-concepts/sandbox/microservices-01/project/project_status/*.txt | head -1)
   ```

2. **Check current sprint priorities**:
   ```bash
   grep -A 10 "## 🎯 Current Sprint" /Volumes/Samsung/mo/projects/research/proof-of-concepts/sandbox/microservices-01/project/TASK.md
   ```

3. **Find any in-progress tasks**:
   ```bash
   grep -l "In Progress" /Volumes/Samsung/mo/projects/research/proof-of-concepts/sandbox/microservices-01/project/tasks/*.md
   ```

Now that you have the context, let's continue our work on the microservices template. We're focusing on a production-ready microservice foundation with auto-configuration capabilities and a comprehensive project management framework.

Our current priorities are:
1. Completing the project management framework integration
2. Implementing the database model foundation
3. Enhancing the health monitoring system

Let's pick up where we left off. What do you suggest we focus on next?