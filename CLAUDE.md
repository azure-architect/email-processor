# Claude Code Guidelines for Python Microservices

## Implementation Best Practices

### 0 — Purpose  

These rules ensure maintainability, safety, and developer velocity for Python microservices. 
**MUST** rules are enforced by CI; **SHOULD** rules are strongly recommended.

---

### 1 — Before Coding

- **BP-1 (MUST)** Ask the user clarifying questions.
- **BP-2 (SHOULD)** Draft and confirm an approach for complex work.  
- **BP-3 (SHOULD)** If ≥ 2 approaches exist, list clear pros and cons.

---

### 2 — While Coding

- **C-1 (MUST)** Follow TDD: scaffold stub -> write failing test -> implement.
- **C-2 (MUST)** Name functions with existing domain vocabulary for consistency.  
- **C-3 (SHOULD NOT)** Introduce classes when small testable functions suffice.  
- **C-4 (SHOULD)** Prefer simple, composable, testable functions.
- **C-5 (MUST)** Use type hints for all function parameters and return values
  ```python
  def get_user_by_id(user_id: UUID) -> User | None:  # ✅ Good
  def get_user_by_id(user_id):                       # ❌ Bad
  ```  
- **C-6 (MUST)** Use `from __future__ import annotations` for forward references in type hints.
- **C-7 (SHOULD NOT)** Add comments except for critical caveats; rely on self‑explanatory code.
- **C-8 (SHOULD)** Use Pydantic models for data validation and serialization.
- **C-9 (SHOULD NOT)** Extract a new function unless it will be reused elsewhere, is the only way to unit-test otherwise untestable logic, or drastically improves readability of an opaque block.
- **C-10 (MUST)** Use async/await for I/O operations (database, HTTP calls, file operations).
- **C-11 (SHOULD)** Follow PEP 8 naming conventions: snake_case for functions/variables, PascalCase for classes.

---

### 3 — Testing

- **T-1 (MUST)** For a simple function, colocate unit tests in `test_*.py` files in same directory or `tests/` subdirectory.
- **T-2 (MUST)** For any API change, add/extend integration tests in `tests/integration/`.
- **T-3 (MUST)** ALWAYS separate pure-logic unit tests from DB-touching integration tests.
- **T-4 (SHOULD)** Prefer integration tests over heavy mocking.  
- **T-5 (SHOULD)** Unit-test complex algorithms thoroughly.
- **T-6 (SHOULD)** Test the entire structure in one assertion if possible
  ```python
  assert result == [expected_value]  # Good

  assert len(result) == 1           # Bad
  assert result[0] == expected_value # Bad
  ```
- **T-7 (MUST)** Use pytest fixtures for test setup and teardown.
- **T-8 (SHOULD)** Use `pytest.mark.asyncio` for async tests.
- **T-9 (MUST)** Use `pytest.mark.parametrize` for testing multiple inputs.

---

### 4 — Database

- **D-1 (MUST)** Type SQLAlchemy queries with proper return types using generics.
- **D-2 (SHOULD)** Use SQLAlchemy's async session for all database operations.
- **D-3 (MUST)** Use dependency injection for database sessions via FastAPI `Depends()`.
- **D-4 (SHOULD)** Use Alembic for database migrations with descriptive revision messages.
- **D-5 (MUST)** Always use transactions for multi-step database operations.

---

### 5 — Code Organization

- **O-1 (MUST)** Place shared code in `src/core/` only if used by ≥ 2 modules.
- **O-2 (SHOULD)** Follow domain-driven design: group related functionality in modules.
- **O-3 (MUST)** Keep route handlers thin; move business logic to service layers.

---

### 6 — Tooling Gates

- **G-1 (MUST)** `black --check .` passes (code formatting).
- **G-2 (MUST)** `ruff check .` passes (linting).
- **G-3 (MUST)** `mypy .` passes (type checking).
- **G-4 (MUST)** `pytest` passes (all tests).

---

### 7 - Git

- **GH-1 (MUST)** Use Conventional Commits format when writing commit messages: https://www.conventionalcommits.org/en/v1.0.0
- **GH-2 (SHOULD NOT)** Refer to Claude or Anthropic in commit messages.

---

## Writing Functions Best Practices

When evaluating whether a function you implemented is good or not, use this checklist:

1. Can you read the function and HONESTLY easily follow what it's doing? If yes, then stop here.
2. Does the function have very high cyclomatic complexity? (number of independent paths, or, in a lot of cases, number of nesting if if-else as a proxy). If it does, then it's probably sketchy.
3. Are there any common data structures and algorithms that would make this function much easier to follow and more robust? Parsers, trees, stacks / queues, etc.
4. Are there any unused parameters in the function?
5. Are there any unnecessary type casts that can be moved to function arguments?
6. Is the function easily testable without mocking core features (e.g. database queries, redis, etc.)? If not, can this function be tested as part of an integration test?
7. Does it have any hidden untested dependencies or any values that can be factored out into the arguments instead? Only care about non-trivial dependencies that can actually change or affect the function.
8. Brainstorm 3 better function names and see if the current name is the best, consistent with rest of codebase.

IMPORTANT: you SHOULD NOT refactor out a separate function unless there is a compelling need, such as:
  - the refactored function is used in more than one place
  - the refactored function is easily unit testable while the original function is not AND you can't test it any other way
  - the original function is extremely hard to follow and you resort to putting comments everywhere just to explain it

## Writing Tests Best Practices

When evaluating whether a test you've implemented is good or not, use this checklist:

1. SHOULD parameterize inputs; never embed unexplained literals such as 42 or "foo" directly in the test.
2. SHOULD NOT add a test unless it can fail for a real defect. Trivial asserts (e.g., `assert 2 == 2`) are forbidden.
3. SHOULD ensure the test description states exactly what the final assert verifies. If the wording and assert don't align, rename or rewrite.
4. SHOULD compare results to independent, pre-computed expectations or to properties of the domain, never to the function's output re-used as the oracle.
5. SHOULD follow the same lint, type-safety, and style rules as prod code (black, ruff, mypy).
6. SHOULD express invariants or axioms (e.g., commutativity, idempotence, round-trip) rather than single hard-coded cases whenever practical. Use `hypothesis` library e.g.
```python
from hypothesis import given, strategies as st
import pytest
from src.utils import calculate_total

@given(st.lists(st.floats(min_value=0, max_value=1000)))
def test_calculate_total_is_commutative(values):
    """Total should be same regardless of order."""
    shuffled = values.copy()
    random.shuffle(shuffled)
    assert calculate_total(values) == calculate_total(shuffled)
```

7. Unit tests for a function should be grouped under `class TestFunctionName:` or in a module `test_function_name.py`.
8. Use `pytest.approx()` for floating-point comparisons.
9. ALWAYS use strong assertions over weaker ones e.g. `assert x == 1` instead of `assert x >= 1`.
10. SHOULD test edge cases, realistic input, unexpected input, and value boundaries.
11. SHOULD NOT test conditions that are caught by the type checker.

## Code Organization

- `src/` - Main application code
  - `src/api/` - FastAPI route handlers and dependencies
  - `src/core/` - Business logic and domain models
  - `src/database/` - Database models and repository patterns
  - `src/tasks/` - Celery task definitions
  - `src/utils/` - Utility functions and helpers
- `tests/` - Test files
  - `tests/unit/` - Pure logic unit tests
  - `tests/integration/` - Tests that touch database/external services
- `alembic/` - Database migrations
- `docker/` - Docker configuration files

## Claude Code Hooks

This project uses Claude Code hooks to automate development workflows. These hooks replace the manual shortcuts previously used.

### Available Hooks

| Hook Name | Trigger | Purpose |
|-----------|---------|---------|
| best_practices_reminder | When "QNEW" is typed | Remind about best practices |
| plan_analysis | When "QPLAN" is typed | Analyze code for planning |
| code_implementation | When "QCODE" is typed | Implement following best practices |
| code_review | When "QCHECK" is typed | Review all code changes |
| function_review | When "QCHECKF" is typed | Review function changes |
| test_review | When "QCHECKT" is typed | Review test changes |
| ux_testing | When "QUX" is typed | Generate UX test scenarios |
| git_commit | When "QGIT" is typed | Prepare commit message |
| python_code_quality_check | After editing .py files | Check Python code quality |
| test_file_check | After editing test files | Check test quality |
| new_file_template | Before creating new .py files | Apply file templates |
| iadpvec_task_proposal | When "PROPOSE_TASK" is typed | Create task proposal |
| iadpvec_task_validation | When "VALIDATE_TASK" is typed | Validate task completion |
| project_status_update | Every 10 messages | Remind about status updates |

### Hook Functionality Reference

The hooks provide the following functionality:

#### QNEW
```
Understand all BEST PRACTICES listed in CLAUDE.md.
Your code SHOULD ALWAYS follow these best practices.
```

#### QPLAN
```
Analyze similar parts of the codebase and determine whether your plan:
- is consistent with rest of codebase
- introduces minimal changes
- reuses existing code
```

#### QCODE
```
Implement your plan and make sure your new tests pass.
Always run tests to make sure you didn't break anything else.
Always run `black .` on the newly created files to ensure standard formatting.
Always run `ruff check .` and `mypy .` to make sure linting and type checking passes.
```

#### QCHECK
```
You are a SKEPTICAL senior software engineer.
Perform this analysis for every MAJOR code change you introduced (skip minor changes):

1. CLAUDE.md checklist Writing Functions Best Practices.
2. CLAUDE.md checklist Writing Tests Best Practices.
3. CLAUDE.md checklist Implementation Best Practices.
```

#### QCHECKF
```
You are a SKEPTICAL senior software engineer.
Perform this analysis for every MAJOR function you added or edited (skip minor changes):

1. CLAUDE.md checklist Writing Functions Best Practices.
```

#### QCHECKT
```
You are a SKEPTICAL senior software engineer.
Perform this analysis for every MAJOR test you added or edited (skip minor changes):

1. CLAUDE.md checklist Writing Tests Best Practices.
```

#### QUX
```
Imagine you are a human UX tester of the feature you implemented. 
Output a comprehensive list of scenarios you would test, sorted by highest priority.
```

#### QGIT
```
Add all changes to staging, create a commit, and push to remote.

Write a text version of the commit message to a timestamped file (format: YYYY-MM-DD_HH-MM-SS.txt) and place it in the project/commit_statements directory.

Follow Conventional Commits format: https://www.conventionalcommits.org/en/v1.0.0
```

### New Workflow Hooks

#### PROPOSE_TASK
Triggers a guided task proposal process following the IADPVEC methodology.

#### VALIDATE_TASK
Triggers a comprehensive task validation process to verify implementation success.

### Customizing Hooks

You can customize the hooks by editing the `.claude/hooks.toml` file. See the [Claude Code documentation](https://docs.anthropic.com/en/docs/claude-code/hooks) for details on hook configuration.
