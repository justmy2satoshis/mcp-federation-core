# Unified Database Architecture Solution

## The Challenge

When pulling MCPs from original repositories:
- Each MCP expects its own database
- Database paths are often hardcoded
- We can't modify the original repositories
- But we want unified database benefits

## Analysis: Which MCPs Actually Need Databases?

### MCPs That Need Persistent Storage (5/15)
1. **memory** - Stores conversation memory
2. **sqlite** - Database interface MCP (special case)
3. **kimi-k2-code-context** - Stores code analysis
4. **kimi-k2-resilient** - Stores resilient data
5. **rag-context** - Stores RAG embeddings

### MCPs That DON'T Need Databases (10/15)
- sequential-thinking (stateless reasoning)
- filesystem (file operations)
- github-manager (API calls)
- web-search (API calls)
- playwright (browser automation)
- git-ops (git operations)
- desktop-commander (system commands)
- perplexity (API calls)
- expert-role-prompt (stateless prompting)
- converse-enhanced (API orchestration)

## Recommended Solution: Selective Unification

### Why Not Full Unification?
- Only 5/15 MCPs actually need databases
- Complexity outweighs benefits for stateless MCPs
- Easier maintenance and updates

### The Hybrid Approach

```
Federation Architecture:
├── Unified Database Group (shared)
│   ├── memory
│   ├── kimi-k2-code-context
│   ├── kimi-k2-resilient
│   └── rag-context
│
├── SQLite MCP (special handler)
│   └── Points to unified database
│
└── Stateless MCPs (no database needed)
    ├── sequential-thinking
    ├── filesystem
    ├── github-manager
    └── ... (7 more)
```

## Implementation Strategy

### Option 1: Environment Variable Override (Preferred)

```python
# In FEDERATED-INSTALLER.py configuration
'memory': {
    'config': {
        'command': 'npx',
        'args': ['-y', '@modelcontextprotocol/server-memory'],
        'env': {
            'MCP_DATABASE': str(self.db_path),  # Unified path
            'SQLITE_PATH': str(self.db_path)
        }
    }
}
```

### Option 2: Wrapper Scripts (For Non-Configurable MCPs)

Create lightweight wrappers that set database paths:

```javascript
// wrapper-memory.js
process.env.DATABASE_URL = '/path/to/unified.db';
require('@modelcontextprotocol/server-memory');
```

### Option 3: Configuration Files

Some MCPs may support config files:

```json
{
  "database": {
    "path": "/path/to/unified.db",
    "shared": true
  }
}
```

## Practical Implementation

### Step 1: Test Configuration Options

```bash
# Test if memory MCP accepts database env var
DATABASE_URL=/tmp/test.db npx -y @modelcontextprotocol/server-memory

# Test if it creates database at specified location
ls -la /tmp/test.db
```

### Step 2: Create Database Schema

```sql
-- Unified database with namespaced tables
CREATE TABLE IF NOT EXISTS memory_data (...);
CREATE TABLE IF NOT EXISTS kimi_code_context (...);
CREATE TABLE IF NOT EXISTS kimi_resilient (...);
CREATE TABLE IF NOT EXISTS rag_embeddings (...);
```

### Step 3: Implement Wrapper for Non-Configurable MCPs

```python
# wrapper_generator.py
def create_wrapper(mcp_name, original_command, db_path):
    wrapper = f"""#!/usr/bin/env node
// Auto-generated wrapper for {mcp_name}
process.env.MCP_DATABASE = '{db_path}';
process.env.DATABASE_URL = '{db_path}';
process.env.SQLITE_PATH = '{db_path}';

// Execute original MCP
const {{ spawn }} = require('child_process');
const mcp = spawn('{original_command}', process.argv.slice(2));
mcp.stdout.pipe(process.stdout);
mcp.stderr.pipe(process.stderr);
mcp.stdin.pipe(process.stdin);
"""
    return wrapper
```

## Performance Analysis

### Unified Database (5 MCPs sharing)
- **Memory**: ~30MB (single connection pool)
- **Disk I/O**: 1 file handle
- **Benefits**: Cross-MCP queries, shared context

### Separate Databases (original)
- **Memory**: ~50MB (5 × 10MB)
- **Disk I/O**: 5 file handles
- **Benefits**: Isolation, simpler

### Conclusion: 40% memory savings for database MCPs

## Architecture Decision

### ✅ Recommended: Selective Unification

**Implement unified database ONLY for MCPs that:**
1. Actually use databases (5/15)
2. Benefit from data sharing
3. Can be configured via env vars or wrappers

**Leave independent:**
- Stateless MCPs (10/15)
- MCPs that don't benefit from sharing

### Benefits of This Approach
- ✅ Maintains ability to pull from original repos
- ✅ Simpler than full unification
- ✅ Still achieves performance benefits where it matters
- ✅ Easier to maintain and debug
- ✅ Graceful fallback if unification fails

## Updated Installer Implementation

```python
class FederatedInstaller:
    def get_mcp_configuration(self, name, mcp_info):
        """Generate config with unified database where applicable"""

        # MCPs that should use unified database
        UNIFIED_DB_MCPS = ['memory', 'kimi-k2-code-context',
                          'kimi-k2-resilient', 'rag-context']

        config = mcp_info['config'].copy()

        if name in UNIFIED_DB_MCPS:
            # Add unified database environment variables
            if 'env' not in config:
                config['env'] = {}

            config['env'].update({
                'MCP_DATABASE': str(self.db_path),
                'DATABASE_URL': f'sqlite:///{self.db_path}',
                'SQLITE_PATH': str(self.db_path),
                'MCP_UNIFIED': 'true'
            })

            # For MCPs that don't respect env vars, use wrapper
            if name in ['kimi-k2-code-context', 'kimi-k2-resilient']:
                wrapper_path = self.create_wrapper(name, config)
                config['command'] = str(wrapper_path)
                config['args'] = []

        return config
```

## Testing Strategy

1. **Install single MCP**: Test database configuration
2. **Verify location**: Check if database created at unified path
3. **Test data sharing**: Write from one MCP, read from another
4. **Performance test**: Measure memory usage and query speed
5. **Update test**: Pull latest from repo, verify still works

## Final Recommendation

**Implement Selective Unification:**
- Use environment variables where supported
- Create thin wrappers for GitHub MCPs
- Unify only the 5 MCPs that use databases
- Document clearly which MCPs share data

This balances the benefits of unified database with the simplicity of maintaining connections to original repositories.