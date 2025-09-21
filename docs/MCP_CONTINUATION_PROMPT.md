# MCP INFRASTRUCTURE CONTINUATION PROMPT - TESTING PHASE
## CRITICAL: READ ENTIRE CONTEXT BEFORE PROCEEDING

### CURRENT STATE AS OF 2025-09-20
All 15 MCPs have been consolidated, fixed, and configured with a unified database system.

### MCP INVENTORY (15 TOTAL)
**Location:** `C:\Users\User\mcp-servers\` (local MCPs)
**Config:** `C:\Users\User\AppData\Roaming\Claude\claude_desktop_config.json`

#### 12 OPERATIONAL NPM MCPs (Already Working):
1. filesystem
2. memory 
3. sequential-thinking
4. desktop-commander
5. perplexity
6. converse
7. rag-context
8. playwright
9. sqlite
10. git-ops
11. github-manager
12. web-search

#### 3 LOCAL MCPs (Fixed & Ready):
13. **expert-role-prompt** (`C:\Users\User\mcp-servers\expert-role-prompt\`)
    - Status: Fixed, has server.js and dependency files
    - Tools: nominate_expert, enhance_prompt, list_expert_roles, execute_workflow
    
14. **kimi-k2-code-context-enhanced** (`C:\Users\User\mcp-servers\kimi-k2-code-context-enhanced\`)
    - Status: Fixed syntax errors, added missing imports
    - Tools: index_repository, search_code, analyze_dependencies, store_context, retrieve_context
    
15. **kimi-k2-resilient-enhanced** (`C:\Users\User\mcp-servers\kimi-k2-resilient-enhanced\`)
    - Status: Fixed, added PerformanceMonitor and CircuitBreaker classes
    - Tools: process_task, get_metrics, store_resilient_data, retrieve_resilient_data, register_webhook

### UNIFIED DATABASE SYSTEM
**Database Path:** `C:\Users\User\mcp-unified.db`
**Table:** `mcp_storage`
**Schema:**
```sql
CREATE TABLE mcp_storage (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    mcp_name TEXT NOT NULL,
    key TEXT NOT NULL,
    value TEXT NOT NULL,
    ttl INTEGER,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    UNIQUE(mcp_name, key)
)
```

### TEST SCRIPT AVAILABLE
**Location:** `C:\Users\User\test_mcp_persistence.py`
- Tests all aspects of data persistence
- Verifies cross-MCP data sharing
- Already run once successfully

### WHAT WAS FIXED IN PREVIOUS SESSION
1. Removed basic Kimi versions (kept only enhanced)
2. Fixed syntax errors (unmatched parentheses) in both Kimi MCPs
3. Added missing MCP server initialization code
4. Fixed InitializationOptions with required parameters
5. Added missing classes (PerformanceMonitor, CircuitBreaker)
6. Integrated unified database in all local MCPs

### TESTING MISSION - VERIFY EVERYTHING WORKS

#### STEP 1: Verify MCP Status in Claude Desktop
Check that all 15 MCPs show as running (no warning triangles)

#### STEP 2: Test Data Storage from Each MCP
Use the following tools to store test data:

1. **From kimi-k2-code-context-enhanced:**
   - Use `store_context` tool with key "test_code_context" and value "Repository indexed at 2025-09-20"

2. **From kimi-k2-resilient-enhanced:**
   - Use `store_resilient_data` tool with key "test_resilient" and value "Circuit breaker status: closed"

3. **From memory MCP:**
   - Store a test memory with key "test_memory" 

4. **From rag-context MCP:**
   - Store test context with key "test_rag"

#### STEP 3: Test Cross-MCP Data Retrieval
1. Use kimi-k2-code-context-enhanced's `retrieve_context` to get data stored by kimi-resilient
2. Use kimi-k2-resilient-enhanced's `retrieve_resilient_data` to get data stored by kimi-code
3. Verify data is shared across MCPs

#### STEP 4: Test Data Persistence
1. Store data with TTL using `store_resilient_data` with ttl=3600
2. Retrieve to confirm TTL is set
3. Test expired data cleanup

#### STEP 5: Run Full Persistence Test
```bash
python C:\Users\User\test_mcp_persistence.py
```

#### STEP 6: Database Verification
Check the unified database directly:
```python
import sqlite3
from pathlib import Path
conn = sqlite3.connect(str(Path.home() / "mcp-unified.db"))
cursor = conn.cursor()
cursor.execute("SELECT mcp_name, key, value FROM mcp_storage")
print(cursor.fetchall())
```

### EXPECTED RESULTS
- All MCPs should successfully store data
- Data should be retrievable by any MCP
- TTL/expiration should work correctly
- Database should show entries from multiple MCPs

### TROUBLESHOOTING
If any MCP shows errors:
1. Check logs at: `C:\Users\User\AppData\Roaming\Claude\logs\mcp-server-*.log`
2. Test servers manually: `python C:\Users\User\mcp-servers\[mcp-name]\server.py`
3. Verify unified database exists: `C:\Users\User\mcp-unified.db`

### SUCCESS CRITERIA
✅ All 15 MCPs running without errors
✅ Data storage works from at least 3 different MCPs
✅ Cross-MCP data retrieval verified
✅ TTL/expiration functioning
✅ Persistence test script passes all tests

### NOTES
- DO NOT simplify or create "simpler versions" of enhanced implementations
- DO NOT delete any working MCPs
- The unified database is the key achievement - all MCPs share `C:\Users\User\mcp-unified.db`
- Previous attempt had 35 MCPs claimed - this was false, we have exactly 15 working MCPs