# IADPVEC Workflow: Task Proposal and Discussion

**Structured workflow for creating comprehensive task proposals that enable informed decision-making before implementation.**

---

## 🎯 **Purpose**

This workflow creates detailed task proposals that provide complete context and analysis before any implementation begins. It ensures developers have full understanding of:
- What will be built and why
- How it fits into existing architecture
- What the implementation approach will be
- What the expected outcomes are

**Key Principle**: No implementation happens without explicit approval of the complete proposal.

---

## 📋 **When to Use This Workflow**

### **Perfect For:**
- **New feature requests** - "Add authentication system"
- **Infrastructure tasks** - "Set up monitoring"
- **Bug fix requests** - "Fix memory leak in worker"
- **Architecture changes** - "Migrate to microservices"
- **Integration tasks** - "Add payment processing"

### **Use When:**
- Developer requests a specific task or feature
- Task complexity is unclear and needs analysis
- Implementation approach needs discussion
- Multiple solutions exist and choice needs validation
- Stakeholder alignment needed before work begins

---

## 🔄 **The Complete Workflow Process**

### **Phase 1: PROPOSED TASK (Task Definition)**

**Format:**
```markdown
## **PROPOSED TASK**

**[Task Title]** - [Brief description with clear objective and scope]
```

**Example:**
```markdown
## **PROPOSED TASK**

**Create FastAPI Application Foundation** - Implement minimal FastAPI application structure to eliminate Docker container errors and establish working foundation for development.
```

**Guidelines:**
- **Clear title** that describes the deliverable
- **Brief description** explaining the objective
- **Scope indication** showing what's included/excluded

---

### **Phase 2: INGEST (Context Analysis)**

**AI Response Format:**
```markdown
## **INGEST: Context Analysis**

I've analyzed the current project state:

✅ **Current Infrastructure**: [What's already working]
✅ **Current Problem**: [Specific issue being addressed]  
✅ **Architecture Guidelines**: [Relevant PLANNING.md requirements]
✅ **Quality Requirements**: [Testing, standards, patterns to follow]
✅ **Integration Points**: [How this connects to existing systems]

**Key Issue**: [Root cause or primary challenge to solve]
```

**AI Checklist:**
- ✅ Read PLANNING.md for architecture context
- ✅ Check TASK.md for related work and priorities
- ✅ Analyze current codebase state
- ✅ Review existing patterns and standards
- ✅ Identify integration requirements
- ✅ Understand quality gates and expectations

---

### **Phase 3: ASSESS (Requirements & Gap Analysis)**

**AI Response Format:**
```markdown
## **ASSESS: Current State & Requirements**

**What's Working:**
- [Existing functionality that works well]
- [Infrastructure already in place]
- [Patterns and standards established]

**What's Missing:**
- [Specific gaps that need to be filled]
- [Missing components or functionality]
- [Technical debt that impacts this work]

**Requirements Analysis:**
- [Must-have functional requirements]
- [Performance and quality requirements]  
- [Integration and compatibility requirements]
- [Security and compliance requirements]
```

**AI Evaluation Criteria:**
- **Functional gaps** - What specific functionality is missing
- **Technical requirements** - Performance, scalability, security needs
- **Integration needs** - How this connects to existing systems
- **Quality standards** - Testing, documentation, code quality expectations
- **Constraints** - Time, resource, or technical limitations

---

### **Phase 4: DISCUSS (Solution Proposal)**

**AI Response Format:**
```markdown
## **DISCUSS: Recommended Implementation Approach**

Based on my analysis and the [relevant documentation], I recommend implementing a **[solution approach]** with these components:

**Proposed Structure:**
```
[Directory/file structure or component breakdown]
```

**Key Features:**
- ✅ **[Feature 1]** - [Description and benefit]
- ✅ **[Feature 2]** - [Description and benefit]
- ✅ **[Feature 3]** - [Description and benefit]

**This approach will:**
- ✅ [Primary benefit and problem resolution]
- ✅ [Secondary benefits and future enablement]
- ✅ [Alignment with existing patterns and standards]

**Technical Considerations:**
- [Important implementation details]
- [Potential challenges and mitigations]
- [Performance or scalability implications]

Shall I proceed with creating a detailed implementation plan for this [solution]?
```

**AI Solution Components:**
- **Clear recommendation** with rationale
- **Specific technical approach** with examples
- **Benefits articulation** showing value
- **Risk consideration** and mitigation strategies
- **Explicit permission request** before proceeding

---

## 🎯 **Developer Response Options**

### **Approval Responses:**
- **"Proceed with the plan"** - Move to PLAN phase
- **"Sounds good, implement this"** - Skip to detailed planning
- **"Yes, go ahead"** - Continue with proposed approach

### **Modification Requests:**
- **"Change [X] to [Y]"** - Adjust specific aspects
- **"Consider [alternative approach]"** - Evaluate different solution
- **"Add [requirement]"** - Include additional features

### **Clarification Requests:**
- **"What about [concern]?"** - Address specific questions
- **"How does this handle [scenario]?"** - Explain edge cases
- **"Why not [alternative]?"** - Compare with other approaches

### **Rejection/Postponement:**
- **"This isn't the right approach"** - Return to ASSESS phase
- **"Let's tackle [other priority] first"** - Defer this task
- **"Too complex, break it down"** - Simplify scope

---

## 📊 **Quality Criteria for Task Proposals**

### **Complete Context Gathering**
- ✅ **Architecture understanding** - Knows how solution fits into system
- ✅ **Current state analysis** - Clear picture of what exists
- ✅ **Requirement identification** - Understands what needs to be built
- ✅ **Pattern awareness** - Follows established project conventions

### **Thorough Assessment**
- ✅ **Gap analysis** - Identifies what's missing vs what's working
- ✅ **Risk evaluation** - Considers potential challenges
- ✅ **Resource estimation** - Understands implementation complexity
- ✅ **Integration planning** - Knows how pieces connect

### **Clear Solution Proposal**
- ✅ **Specific approach** - Concrete technical solution proposed
- ✅ **Structured breakdown** - Components and organization clear
- ✅ **Benefit articulation** - Value proposition explained
- ✅ **Implementation preview** - Developer knows what will be built

### **Decision-Ready Information**
- ✅ **Complete picture** - All necessary information provided
- ✅ **Clear options** - Approach and alternatives considered
- ✅ **Risk transparency** - Challenges and mitigations identified
- ✅ **Permission seeking** - Explicit approval requested

---

## 🔄 **Integration with Full IADPVEC Workflow**

### **This Workflow Covers: INGEST → ASSESS → DISCUSS**
```
PROPOSED TASK → INGEST → ASSESS → DISCUSS → [DEVELOPER APPROVAL]
                                                    ↓
                                           PLAN → VALIDATE → EXECUTE → COMMIT
```

### **Transition to Implementation**
Once developer approves the proposal:
1. **PLAN**: Create detailed implementation plan with specific files and steps
2. **VALIDATE**: Define success criteria and testing approach  
3. **EXECUTE**: Implement according to approved plan
4. **COMMIT**: Document and commit changes with full context

### **Workflow Benefits**
- **Informed decisions** - Developer knows exactly what will be built
- **Reduced rework** - Solution validated before implementation
- **Better architecture** - Considers integration and patterns upfront
- **Clear communication** - Transparent process with explicit approval points

---

## 📝 **Example Task Proposal Templates**

### **Feature Implementation Template**
```markdown
## **PROPOSED TASK**
**[Feature Name]** - [Description of functionality to be added]

## **INGEST: Context Analysis**
✅ **Current State**: [What exists now]
✅ **User Need**: [Why this feature is needed]
✅ **Architecture Fit**: [How it integrates with existing system]

## **ASSESS: Requirements & Gaps**
**What's Working**: [Existing related functionality]
**What's Missing**: [Specific gaps this feature fills]
**Requirements**: [Functional and technical requirements]

## **DISCUSS: Implementation Approach**
**Proposed Solution**: [Technical approach]
**Key Components**: [Major pieces to be built]
**Benefits**: [Value delivered]
**Considerations**: [Implementation challenges]
```

### **Bug Fix Template**
```markdown
## **PROPOSED TASK**
**Fix [Problem Description]** - [Resolution approach]

## **INGEST: Context Analysis**
✅ **Issue Identification**: [Root cause analysis]
✅ **Impact Assessment**: [Who/what is affected]
✅ **Current Workarounds**: [Temporary solutions in place]

## **ASSESS: Root Cause & Requirements**
**Problem Analysis**: [Technical details of the issue]
**Fix Requirements**: [What the solution must accomplish]
**Testing Needs**: [How to verify the fix works]

## **DISCUSS: Resolution Approach**
**Proposed Fix**: [Technical solution]
**Testing Strategy**: [Validation approach]
**Risk Mitigation**: [Ensuring fix doesn't break other things]
```

### **Infrastructure Task Template**
```markdown
## **PROPOSED TASK**
**Setup [Infrastructure Component]** - [Purpose and scope]

## **INGEST: Context Analysis**
✅ **Current Infrastructure**: [What's already deployed]
✅ **Integration Requirements**: [How this fits into existing setup]
✅ **Operational Needs**: [Monitoring, maintenance, scaling]

## **ASSESS: Requirements & Implementation**
**Infrastructure Gaps**: [What's missing]
**Technical Requirements**: [Performance, security, reliability]
**Operational Requirements**: [Deployment, monitoring, maintenance]

## **DISCUSS: Implementation Strategy**
**Proposed Architecture**: [Technical design]
**Deployment Plan**: [How it will be implemented]
**Operational Integration**: [Monitoring, alerting, maintenance]
```

---

## 🚀 **Best Practices**

### **For AI Assistants**
- **Be thorough** in context gathering - read all relevant documentation
- **Be specific** in proposals - concrete technical solutions, not vague concepts
- **Be honest** about complexity and risks - don't oversimplify challenging work
- **Be explicit** about seeking approval - never assume permission to proceed

### **For Developers**
- **Review proposals carefully** - This is your chance to guide the approach
- **Ask clarifying questions** - Better to discuss upfront than rework later
- **Consider alternatives** - AI proposals are starting points, not final answers
- **Give clear approval** - Explicit "proceed" signals keep workflow moving

### **For Teams**
- **Use for complex tasks** - Simple tasks may not need full proposal workflow
- **Share proposals** - Team members can review and provide input
- **Document decisions** - Capture why certain approaches were chosen
- **Iterate on process** - Improve proposal quality based on outcomes

---

## 📈 **Success Metrics**

### **Quality Indicators**
- **Reduced rework** - Less implementation changes after approval
- **Faster development** - Clear direction accelerates implementation
- **Better architecture** - Solutions consider integration and patterns
- **Team alignment** - Everyone understands what's being built

### **Process Efficiency**
- **Quick approvals** - Well-structured proposals get faster decisions
- **Fewer questions** - Complete analysis reduces back-and-forth
- **Clear expectations** - Developers know exactly what they're approving
- **Smooth transitions** - Approved proposals flow seamlessly to implementation

---

**This workflow ensures every task begins with complete understanding and explicit approval, leading to higher quality implementations with fewer surprises and better architectural decisions.**

---

*Use this workflow whenever a task request needs comprehensive analysis and structured discussion before implementation begins.*