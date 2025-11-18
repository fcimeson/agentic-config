# Context Management Strategy

## Session-Based Isolation

### Purpose
Prevent concurrent agent instances from interfering with each other by using isolated session folders.

### Session Structure
```
.tmp/sessions/{session-id}/{task-category}/{task-name}-context.md
```

### Session ID Format
`{timestamp}-{random-4-chars}`

Example: `20250118-143022-a4f2`

### Session Manifest
Each session has a manifest file tracking all context files:

**Location**: `.tmp/sessions/{session-id}/.manifest.json`

**Structure**:
```json
{
  "session_id": "20250118-143022-a4f2",
  "created_at": "2025-01-18T14:30:22Z",
  "last_activity": "2025-01-18T14:35:10Z",
  "context_files": {
    "features/user-auth-context.md": {
      "created": "2025-01-18T14:30:22Z",
      "for": "@subagents/core/task-manager",
      "keywords": ["user-auth", "authentication", "features"]
    },
    "tasks/user-auth-tasks.md": {
      "created": "2025-01-18T14:32:15Z",
      "for": "@subagents/core/task-manager",
      "keywords": ["user-auth", "tasks", "breakdown"]
    },
    "documentation/api-docs-context.md": {
      "created": "2025-01-18T14:35:10Z",
      "for": "@subagents/core/documentation",
      "keywords": ["api", "documentation"]
    }
  },
  "context_index": {
    "user-auth": [
      "features/user-auth-context.md",
      "tasks/user-auth-tasks.md"
    ],
    "api": [
      "documentation/api-docs-context.md"
    ]
  }
}
```

## Temporary Context Files

### When to Create
Only create context files when **ALL** of these apply:
- Delegating to a subagent
- Context description is verbose (>2 sentences) OR
- Risk of misinterpretation without detailed context

### File Structure
```
.tmp/sessions/{session-id}/{task-category}/{task-name}-context.md
```

### Categories
- `features/` - Feature development context
- `documentation/` - Documentation tasks
- `code/` - Code-related tasks
- `refactoring/` - Refactoring tasks
- `testing/` - Testing tasks
- `tasks/` - Task breakdowns created by task-manager
- `general/` - General tasks that don't fit other categories

### Examples
```
.tmp/sessions/20250118-143022-a4f2/features/user-auth-context.md
.tmp/sessions/20250118-143022-a4f2/documentation/api-docs-context.md
.tmp/sessions/20250118-150000-b7k9/code/database-refactor-context.md
.tmp/sessions/20250118-151500-c3x8/testing/integration-tests-context.md
```

### File Contents
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
```

## Cleanup Strategy

### During Session
1. Remove individual context files after task completion
2. Update manifest to remove file entry
3. Update `last_activity` timestamp

### End of Session
1. Remove entire session folder: `.tmp/sessions/{session-id}/`
2. Only delete files tracked in current session's manifest

### Stale Session Cleanup
- Automatically clean sessions older than 24 hours with no activity
- Check `last_activity` timestamp in manifest
- Safe to run periodically without affecting active sessions

### Manual Cleanup
Users can safely delete:
- Entire `.tmp/` folder anytime
- Individual session folders
- Stale sessions (check `last_activity` timestamp)

## Concurrent Safety

### Isolation Guarantees
✅ Each agent instance has unique session ID
✅ Context files are isolated per session
✅ Manifest tracks only files created by this session
✅ Cleanup only affects current session's files
✅ No risk of deleting another instance's context

### Best Practices
1. **Generate session ID early** - At first context file creation
2. **Track all files** - Add every context file to manifest
3. **Update activity** - Touch `last_activity` on each operation
4. **Clean up promptly** - Remove files after task completion
5. **Only clean own files** - Never delete files outside current session

## Dynamic Context Loading

### Purpose
Allow subagents to discover and load relevant context files created earlier in the session.

### How It Works

**1. Context File Creation**
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

**2. Context Indexing**
Manifest maintains keyword index for fast lookup:
```json
"context_index": {
  "user-auth": [
    "features/user-auth-context.md",
    "tasks/user-auth-tasks.md"
  ]
}
```

**3. Context Discovery**
When delegating to subagent:
1. Search manifest for related context files (by keyword/category)
2. Pass relevant context file paths to subagent
3. Subagent reads context files as needed

**4. Delegation Pattern**
```
Delegating to @subagents/code/coder-agent:
"Implement user authentication login component.

Related context available at:
- .tmp/sessions/20250118-143022-a4f2/features/user-auth-context.md
- .tmp/sessions/20250118-143022-a4f2/tasks/user-auth-tasks.md

Read these files for full context on requirements and task breakdown."
```

### Example Workflow

```
1. User: "Build user authentication system"
   → OpenAgent creates: features/user-auth-context.md
   → Delegates to @task-manager
   
2. Task-manager creates: tasks/user-auth-tasks.md
   → Both files tracked in manifest with keyword "user-auth"
   
3. User: "Implement the login component"
   → OpenAgent searches manifest for "user-auth" context
   → Finds both context files
   → Delegates to @coder-agent with references to both files
   → Coder-agent reads files to understand full context
```

### Benefits
- **No context loss**: Information persists across subagent calls
- **Automatic discovery**: Related context found by keywords
- **Flexible**: Subagents read only what they need
- **Traceable**: Manifest shows all context relationships

---

## Why This Approach?

### Session Isolation
- **Concurrent safety**: Multiple agents can run simultaneously
- **No conflicts**: Each session has its own namespace
- **Easy cleanup**: Delete entire session folder when done
- **Traceable**: Manifest shows what belongs to each session

### Dynamic Context
- **Discoverable**: Context files indexed by keywords
- **Reusable**: Later subagents can access earlier context
- **Flexible**: Load only relevant context
- **Persistent**: Context survives across subagent calls

### Why `.tmp/sessions/`?
- Standard `.tmp/` convention (commonly ignored)
- `sessions/` subfolder makes purpose clear
- Session ID provides unique namespace
- Easy to identify and clean up stale sessions
- Hidden folder (starts with `.`)

## Example Workflow

```bash
# Agent Instance 1 starts
Session ID: 20250118-143022-a4f2
Creates: .tmp/sessions/20250118-143022-a4f2/features/user-auth-context.md

# Agent Instance 2 starts (concurrent)
Session ID: 20250118-143030-b7k9
Creates: .tmp/sessions/20250118-143030-b7k9/features/payment-context.md

# Both agents work independently without conflicts

# Agent Instance 1 completes
Deletes: .tmp/sessions/20250118-143022-a4f2/ (entire folder)

# Agent Instance 2 continues unaffected
Still has: .tmp/sessions/20250118-143030-b7k9/
```
