# Context Discovery

## Purpose

**Dynamically load relevant context files when delegating to subagents**

Allows subagents to discover and access context created earlier in the session, preventing information loss across delegation boundaries.

## How It Works

### 1. Context File Creation

When creating a context file, add metadata to manifest:

```json
"context_files": {
  "features/user-auth-context.md": {
    "created": "2025-01-18T14:30:22Z",
    "for": "@subagents/core/task-manager",
    "keywords": ["user-auth", "authentication", "features"]
  }
}
```

**Metadata Fields**:
- `created`: Timestamp of file creation
- `for`: Target subagent (which agent will use this)
- `keywords`: Array of searchable keywords for discovery

### 2. Context Indexing

Manifest maintains keyword index for fast lookup:

```json
"context_index": {
  "user-auth": [
    "features/user-auth-context.md",
    "tasks/user-auth-tasks.md"
  ],
  "api": [
    "documentation/api-docs-context.md"
  ]
}
```

**Index Structure**:
- Key: Keyword (from context file metadata)
- Value: Array of file paths containing that keyword

### 3. Context Discovery Process

When delegating to subagent:

1. **Extract keywords** from user request or task context
2. **Search manifest** `context_index` for matching keywords
3. **Find related files** by category or keyword match
4. **Pass file paths** to subagent in delegation prompt
5. **Subagent reads** context files as needed

### 4. Delegation Pattern

**Context Reference Format**:
```
Related context available at: .tmp/sessions/{session-id}/features/user-auth-context.md
```

**Full Delegation Example**:
```
Delegating to @subagents/code/coder-agent:

"Implement user authentication login component.

Related context available at:
- .tmp/sessions/20250118-143022-a4f2/features/user-auth-context.md
- .tmp/sessions/20250118-143022-a4f2/tasks/user-auth-tasks.md

Read these files for full context on requirements and task breakdown."
```

## When to Create Context Files

**Only create when ALL of these apply**:
- Delegating to a subagent
- Context description is verbose (>2 sentences) OR
- Risk of misinterpretation without detailed context

**Don't create for**:
- Simple, one-line instructions
- Direct execution (no delegation)
- Conversational questions

## Context File Categories

```
features/     - Feature development context
documentation/ - Documentation tasks
code/         - Code-related tasks
refactoring/  - Refactoring tasks
testing/      - Testing tasks
tasks/        - Task breakdowns created by task-manager
general/      - General tasks that don't fit other categories
```

## Context File Template

```markdown
# Context: {Task Name}
Session: {session-id}

## Request Summary
[Brief description of what needs to be done]

## Background
[Relevant context and information]

## Expected Output
[What the subagent should produce]

## Constraints
[Any limitations or requirements]

## Related Context
[Links to other context files if applicable]
```

## Discovery Strategies

### By Keyword
Search `context_index` for exact keyword matches:
```
User: "Add login validation"
Keywords: ["login", "validation", "user-auth"]
→ Finds: features/user-auth-context.md, tasks/user-auth-tasks.md
```

### By Category
Search `context_files` for matching category:
```
Delegating to @documentation agent
Category: "documentation"
→ Finds all files in documentation/ folder
```

### By Target Agent
Search `context_files` for files created for specific agent:
```
Delegating to @task-manager
Filter: "for": "@subagents/core/task-manager"
→ Finds all context files created for task-manager
```

## Example Workflow

```
1. User: "Build user authentication system"
   → OpenAgent creates: features/user-auth-context.md
   → Manifest updated with keywords: ["user-auth", "authentication", "features"]
   → Delegates to @task-manager with context file path
   
2. Task-manager creates: tasks/user-auth-tasks.md
   → Manifest updated with keywords: ["user-auth", "tasks", "breakdown"]
   → Both files now indexed under "user-auth"
   
3. User: "Implement the login component"
   → OpenAgent searches manifest for "user-auth" OR "login"
   → Finds: features/user-auth-context.md, tasks/user-auth-tasks.md
   → Delegates to @coder-agent with references to BOTH files
   → Coder-agent reads both files to understand full context
   
4. User: "Add password reset feature"
   → OpenAgent searches manifest for "user-auth" OR "password"
   → Finds existing user-auth context
   → Creates new: features/password-reset-context.md
   → Links to existing user-auth context
   → Delegates with all related context files
```

## Benefits

✅ **No context loss**: Information persists across subagent calls
✅ **Automatic discovery**: Related context found by keywords
✅ **Flexible**: Subagents read only what they need
✅ **Traceable**: Manifest shows all context relationships
✅ **Scalable**: Works with multiple context files per session
✅ **Reusable**: Later tasks can reference earlier context

## Context Inheritance

**Load related context files from manifest before delegating**

When delegating to a subagent:
1. Check if session exists
2. Read manifest if available
3. Search for related context by keyword/category
4. Include relevant context file paths in delegation
5. Subagent reads context files as first step

This ensures subagents have full context from earlier in the session.

## Error Handling

### Manifest Not Found
- Session not initialized yet
- Continue without context discovery
- Create new session if context file needed

### Context File Missing
- File was deleted or moved
- Warn user about missing context
- Continue with available context
- Update manifest to remove missing file

### Keyword Collision
- Multiple files match same keyword
- Include all matching files in delegation
- Let subagent determine relevance
- Consider more specific keywords in future

## Best Practices

1. **Use specific keywords**: "user-auth" better than "auth"
2. **Include category in keywords**: ["features", "user-auth"]
3. **Link related context**: Reference other context files
4. **Update manifest immediately**: Don't delay indexing
5. **Clean up stale context**: Remove when task complete
6. **Validate file exists**: Before passing to subagent
