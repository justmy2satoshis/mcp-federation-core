# MCP CLAUDE CODE INTEGRATION - CONTINUATION PROMPT

## 📊 CURRENT STATUS (2025-09-21 8:45 AM Sydney)

### ✅ COMPLETED IN PREVIOUS CHAT:
1. **Consolidated MCP Directory Structure**:
   - All MCPs moved to `C:\Users\User\mcp-servers\`
   - Organized into: servers\, databases\, configs\, scripts\, docs\, logs\, workspace\
   - Databases unified in databases\ folder

2. **Claude Code Installed & Partially Configured**:
   - Version: 1.0.120
   - 3 of 15 MCPs connected successfully:
     - expert-role-prompt (Node.js)
     - kimi-k2-resilient (Python)
     - kimi-k2-code-context (Python)

3. **Key Understanding**:
   - Claude Desktop and Claude Code have separate configs
   - Desktop: `AppData\Roaming\Claude\claude_desktop_config.json`
   - Code: `.claude.json` (project-specific)
   - Processes can't be shared (stdio limitation) but databases can

---

## 🎯 OBJECTIVES FOR THIS CHAT

### Phase 1: Set Working Directory
Provide command lines to properly set Claude Code's working directory to `C:\Users\User\mcp-servers\workspace`

### Phase 2: Generate JSON Prompt for Claude Code
Create a comprehensive JSON prompt that will instruct Claude Code (CCC-VS) to:
1. Audit existing MCP configurations
2. Identify the remaining 12 MCPs from Claude Desktop
3. Add them to Claude Code configuration
4. Test each MCP for connectivity
5. Document any issues or missing dependencies

### Phase 3: MCP Parity Achievement
Add the remaining 12 MCPs to Claude Code:
- Context7
- converse  
- memory
- filesystem
- perplexity
- desktop-commander
- web-search
- sqlite
- playwright
- github-manager
- git-ops
- rag-context

### Phase 4: Testing & Verification
Test all 15 MCPs in Claude Code to ensure full parity with Claude Desktop

### Phase 5: New MCP Installation
After parity, install additional MCPs from the prioritized list:
**Priority 1**: docker, terraform, linear, notion, airtable, vercel
**Priority 2**: slack, discord, jira, confluence, asana
**Priority 3**: aws-s3, azure-cognitive, openai, langchain, pinecone
**Priority 4**: redis, elasticsearch, kubernetes, grafana, prometheus
**Priority 5**: google-maps, spotify, stripe, twilio, sendgrid

---

## 📁 KEY PATHS & LOCATIONS

```
Working Directory: C:\Users\User\mcp-servers\workspace
MCP Servers: C:\Users\User\mcp-servers\servers\
Databases: C:\Users\User\mcp-servers\databases\
Claude Desktop MCPs: Check AppData\Roaming\Claude\claude_desktop_config.json
Claude Code Config: C:\Users\User\.claude.json
```

---

## 💻 COMMAND SEQUENCE NEEDED

### 1. Set Working Directory Commands:
```bash
cd C:\Users\User\mcp-servers\workspace
claude config list
```

### 2. Check Claude Desktop Configuration:
Need to examine `claude_desktop_config.json` to identify all 15 MCPs and their exact configurations

### 3. Add Missing MCPs:
For each MCP, determine:
- Is it Node.js (server.js) or Python (server.py)?
- What's the exact path?
- Any special arguments or environment variables?

---

## 📝 JSON PROMPT STRUCTURE FOR CLAUDE CODE

The JSON prompt should follow this structure:
```json
{
  "task": "Complete MCP integration for Claude Code CLI",
  "context": {
    "current_mcps": 3,
    "target_mcps": 15,
    "working_directory": "C:\\Users\\User\\mcp-servers\\workspace"
  },
  "steps": [
    {
      "step": 1,
      "action": "audit_current_state",
      "commands": ["claude mcp list", "dir C:\\Users\\User\\mcp-servers\\servers"]
    },
    {
      "step": 2,
      "action": "read_desktop_config",
      "path": "C:\\Users\\User\\AppData\\Roaming\\Claude\\claude_desktop_config.json"
    },
    {
      "step": 3,
      "action": "add_missing_mcps",
      "validate_each": true
    },
    {
      "step": 4,
      "action": "test_all_mcps",
      "expected_count": 15
    }
  ]
}
```

---

## ⚠️ IMPORTANT NOTES

1. **Check MCP Types**: Some are Node.js (server.js), some are Python (server.py)
2. **Handle Locked Files**: rag-context MCP has locked memories.db - use copied version
3. **Resource Monitoring**: Watch for process count increases during testing
4. **Shared Resources**: Databases in databases\ folder are shared between Desktop & Code

---

## 🎯 SUCCESS CRITERIA

1. All 15 MCPs from Claude Desktop working in Claude Code
2. Proper working directory set
3. JSON prompt successfully guides Claude Code through integration
4. All MCPs pass connectivity test
5. Ready to install Priority 1 new MCPs

---

## 🔧 TROUBLESHOOTING REFERENCE

If an MCP fails to connect:
1. Check if it needs node vs python
2. Verify the server file exists (server.js or server.py)
3. Check for missing dependencies (npm install or pip install)
4. Look for any required environment variables
5. Ensure database paths are updated to new location

---

## 📊 PROCESS MONITORING

Current state:
- Claude Desktop: ~49 Node.js processes (persistent)
- Claude Code: 0 processes when idle, 3-5 when running
- Expected during full test: ~52-54 processes temporarily

---

BEGIN NEW CHAT WITH THIS CONTEXT. First action: Set working directory and examine Claude Desktop configuration to map all 15 MCPs.
