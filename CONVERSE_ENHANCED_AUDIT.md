# Converse-Enhanced MCP Audit Report

## Executive Summary
- **Status**: Functional but using outdated model versions
- **14/15 MCPs**: Working perfectly (DO NOT TOUCH)
- **Converse-Enhanced**: Working but needs model updates in its repository

## 1. Current State Analysis

### Configuration in Installer (v0.1.5)
```python
'converse-enhanced': {
    'type': 'github',
    'source': 'https://github.com/justmy2satoshis/converse-mcp-enhanced.git',
    'directory': 'converse-mcp-enhanced',
    'branch': 'main',
    'install': ['pip', 'install', '-r', 'requirements.txt'],
    'needs_db': False,
    'config': {
        'command': 'python',
        'args': [str(self.base_dir / 'converse-mcp-enhanced' / 'src' / 'server.py')],
        'env': {
            'OPENAI_API_KEY': 'YOUR_OPENAI_KEY',
            'GEMINI_API_KEY': 'YOUR_GEMINI_KEY'
        }
    }
}
```

**✅ CORRECT**: Uses Python, proper path, placeholder API keys

## 2. Model Version Findings

### Currently Hardcoded Models (OUTDATED)
```python
# In src/server.py
models=["claude-3-opus-20240229", "claude-3-sonnet-20240229", "claude-3-haiku-20240307"]
models=["gpt-4", "gpt-3.5-turbo", "gpt-4-turbo-preview"]
models=["gemini-pro", "gemini-pro-vision"]
models=["grok-1", "grok-2"]
models=["pplx-7b-online", "pplx-70b-online"]
```

### Should Be Updated To
```python
models=["claude-opus-4-1-20250805", "claude-sonnet-4", "claude-haiku-3"]
models=["gpt-5", "gpt-4-turbo", "gpt-3.5-turbo"]
models=["gemini-2.0-pro", "gemini-2.0-flash"]
models=["grok-2", "grok-1"]
models=["pplx-70b-online", "pplx-7b-online"]
```

## 3. API Key Handling

### Current Implementation (CORRECT)
- ✅ Installer uses placeholders: `YOUR_OPENAI_KEY`, `YOUR_GEMINI_KEY`
- ✅ Server reads from environment variables: `os.getenv("OPENAI_API_KEY")`
- ✅ Graceful handling of missing keys (provider disabled if no key)
- ✅ Users update keys post-install by editing `claude_desktop_config.json`

**NO CHANGES NEEDED** for API key handling

## 4. Critical Issues

### Issue 1: Missing requirements.txt
- The repository has NO `requirements.txt` file
- Installer tries to run: `pip install -r requirements.txt`
- This will FAIL during installation

### Issue 2: Outdated Model Versions
- Using Claude 3 models from March 2024
- No GPT-5 support
- Old Gemini models

## 5. Recommendations

### IMMEDIATE FIX NEEDED (Critical)
Create `requirements.txt` in converse-enhanced repository:
```txt
httpx>=0.24.0
python-dotenv>=1.0.0
```

### MODEL UPDATES (Important)
Update `src/server.py` in converse-enhanced repository:
1. Line ~70-75: Update Anthropic models to Claude 4
2. Line ~80-85: Update OpenAI models to include GPT-5
3. Line ~90-95: Update Google models to Gemini 2.0

### DO NOT CHANGE
- ❌ DO NOT modify FEDERATED-INSTALLER-UNIFIED.py (it's working!)
- ❌ DO NOT touch the 14 working MCPs
- ❌ DO NOT add complexity to the installer

## 6. Action Plan

### Option A: Fix Repository Directly (RECOMMENDED)
1. Fork/update https://github.com/justmy2satoshis/converse-mcp-enhanced
2. Add missing `requirements.txt`
3. Update model strings in `src/server.py`
4. Test independently before any installer changes

### Option B: Document Workaround
1. Tell users to create `requirements.txt` manually after cloning
2. Provide instructions for updating model strings post-install
3. Keep installer unchanged

### Option C: Minimal Installer Fix
ONLY if Option A fails:
1. Change install command from `['pip', 'install', '-r', 'requirements.txt']`
2. To: `['pip', 'install', 'httpx', 'python-dotenv']`
3. This bypasses missing requirements.txt

## 7. Testing Protocol

Before ANY changes:
1. Backup current working installer
2. Test converse-enhanced in isolation
3. Verify 14 other MCPs still work
4. Only then update if needed

## 8. User Instructions (Current Workaround)

### For Missing requirements.txt
After installation fails on converse-enhanced:
```bash
cd ~/mcp-servers/converse-mcp-enhanced
pip install httpx python-dotenv
```

### For API Keys
Edit `~/AppData/Roaming/Claude/claude_desktop_config.json`:
- Replace `YOUR_OPENAI_KEY` with actual OpenAI API key
- Replace `YOUR_GEMINI_KEY` with actual Google API key
- Add `ANTHROPIC_API_KEY` if needed

### For Model Updates
Edit `~/mcp-servers/converse-mcp-enhanced/src/server.py`:
- Search for "claude-3" and update to "claude-opus-4-1-20250805"
- Search for "gpt-4" and update to "gpt-5"
- Save and restart Claude Desktop

## Conclusion

The installer is WORKING for 14/15 MCPs. Converse-enhanced has two issues:
1. **Critical**: Missing requirements.txt (causes installation failure)
2. **Important**: Outdated model versions

**Recommendation**: Fix the converse-enhanced repository directly. DO NOT modify the installer unless absolutely necessary.