# MCP Federation Core v0.1.7 Documentation

## Complete Federation of 16 MCPs with GitHub Source Links

### Overview
The MCP Federation Core unifies 16 specialized Model Context Protocol servers, providing comprehensive capabilities for Claude Desktop. Each MCP is sourced from its original repository for maximum compatibility and updateability.

### Installation
```bash
git clone https://github.com/justmy2satoshis/mcp-federation-core.git
cd mcp-federation-core
python FEDERATED-INSTALLER-UNIFIED.py
```

## All 16 Federated MCPs with Source Links

### 1. Sequential Thinking MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@modelcontextprotocol/server-sequential-thinking)
- **Type**: NPM
- **Description**: Chain-of-thought and tree-of-thought reasoning
- **Command**: `npx -y @modelcontextprotocol/server-sequential-thinking`

### 2. Memory MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@modelcontextprotocol/server-memory)
- **Type**: NPM (Unified DB)
- **Description**: Persistent conversation memory with unified database
- **Command**: `npx -y @modelcontextprotocol/server-memory`

### 3. Filesystem MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@modelcontextprotocol/server-filesystem)
- **Type**: NPM
- **Description**: File system operations and management
- **Command**: `npx -y @modelcontextprotocol/server-filesystem`

### 4. SQLite MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/mcp-sqlite)
- **Type**: NPM
- **Description**: SQLite database interface (powers unified DB)
- **Command**: `npx -y mcp-sqlite`

### 5. GitHub Manager MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@modelcontextprotocol/server-github)
- **Type**: NPM
- **Description**: GitHub repository management and operations
- **Command**: `npx -y @modelcontextprotocol/server-github`
- **Env**: `GITHUB_TOKEN`

### 6. Web Search MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@modelcontextprotocol/server-brave-search)
- **Type**: NPM
- **Description**: Brave Search API integration
- **Command**: `npx -y @modelcontextprotocol/server-brave-search`
- **Env**: `BRAVE_API_KEY`

### 7. Playwright MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@playwright/mcp)
- **Type**: NPM
- **Description**: Browser automation and web scraping
- **Command**: `npx -y @playwright/mcp@0.0.39 --browser chromium`

### 8. Git Operations MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@cyanheads/git-mcp-server)
- **Type**: NPM
- **Description**: Comprehensive Git operations
- **Command**: `npx -y @cyanheads/git-mcp-server`

### 9. Desktop Commander MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@wonderwhy-er/desktop-commander)
- **Type**: NPM
- **Description**: Desktop automation and system commands
- **Command**: `npx -y @wonderwhy-er/desktop-commander@latest`

### 10. Perplexity MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/server-perplexity-ask)
- **Type**: NPM
- **Description**: Perplexity AI integration
- **Command**: `npx -y server-perplexity-ask`
- **Env**: `PERPLEXITY_API_KEY`

### 11. Expert Role Prompt MCP
- **Source**: [GitHub Repository](https://github.com/justmy2satoshis/expert-role-prompt-mcp)
- **Type**: GitHub (Node.js)
- **Description**: Expert role selection and prompt enhancement
- **Command**: `node ~/mcp-servers/expert-role-prompt/server.js`
- **Fixed**: v0.1.4 - Role ID validation now handles underscores/hyphens correctly

### 12. Converse Enhanced MCP
- **Source**: [GitHub Repository](https://github.com/justmy2satoshis/converse-mcp-enhanced)
- **Type**: GitHub (Python)
- **Description**: Multi-model conversation management with Ollama support
- **Command**: `python ~/mcp-servers/converse-mcp-enhanced/src/server.py`
- **Env**: `OPENAI_API_KEY`, `GEMINI_API_KEY`
- **Fixed**: v0.1.6 - Direct dependency installation (httpx, python-dotenv)

### 13. Kimi K2 Code Context MCP
- **Source**: [GitHub Repository](https://github.com/justmy2satoshis/kimi-k2-code-context-mcp-repo)
- **Type**: GitHub (Python, Unified DB)
- **Description**: Code context management and analysis
- **Command**: `python ~/mcp-servers/kimi-k2-code-context-enhanced/server.py`

### 14. Kimi K2 Resilient MCP
- **Source**: [GitHub Repository](https://github.com/justmy2satoshis/kimi-k2-heavy-processor-mcp-repo)
- **Type**: GitHub (Python, Unified DB)
- **Description**: Heavy computation and processing tasks
- **Command**: `python ~/mcp-servers/kimi-k2-resilient-enhanced/server.py`

### 15. RAG Context MCP
- **Source**: [NPM Package](https://www.npmjs.com/package/@notbnull/mcp-rag-context)
- **Type**: NPM (Unified DB)
- **Description**: Retrieval-Augmented Generation context management
- **Command**: `npx -y @notbnull/mcp-rag-context`

### 16. RAG-Anything MCP *(NEW)*
- **Source**: [GitHub Repository](https://github.com/justmy2satoshis/rag-anything-mcp)
- **Type**: GitHub (Node.js/TypeScript)
- **Description**: Multimodal document processing with knowledge graphs
- **Command**: `node ~/mcp-servers/rag-anything-mcp/dist/index.js`
- **Features**:
  - Handles PDFs, images, tables, equations
  - Automatic entity extraction
  - Knowledge graph visualization
  - Multiple query modes (naive, local, global, hybrid)
- **Env**: `RAG_LLM_PROVIDER`, `RAG_MODEL_NAME`, `RAG_EMBED_MODEL`

## Unified Database Architecture

The federation implements selective database unification for MCPs that benefit from shared context:

### Unified DB MCPs (40% memory savings):
- Memory MCP
- Kimi K2 Code Context
- Kimi K2 Resilient
- RAG Context

### Database Location:
`~/mcp-servers/mcp-unified.db`

## Environment Variables

Add to your shell profile (.bashrc, .zshrc, or Windows Environment):

```bash
# Required API Keys
export GITHUB_TOKEN="your_github_token"
export BRAVE_API_KEY="your_brave_api_key"
export PERPLEXITY_API_KEY="your_perplexity_key"
export OPENAI_API_KEY="your_openai_key"
export GEMINI_API_KEY="your_gemini_key"

# RAG-Anything Configuration (Optional)
export RAG_LLM_PROVIDER="openai"
export RAG_MODEL_NAME="gpt-4"
export RAG_EMBED_MODEL="text-embedding-3-small"
```

## Version History

### v0.1.7 (Current)
- Added RAG-Anything as 16th Federated MCP
- Complete GitHub source links for all MCPs
- Multimodal document processing support

### v0.1.6
- Fixed converse-enhanced dependency installation

### v0.1.5
- Fixed converse-enhanced to use Python server

### v0.1.4
- Fixed expert-role-prompt validation issues
- Fixed directory nesting bug
- Updated all MCP commands

### v0.1.3
- Safe uninstall preserving user MCPs
- Backup system implementation

## Troubleshooting

### Common Issues:

1. **Expert Role Validation Error**:
   - Fixed in v0.1.4: Now accepts both "backend_engineer" and "backend-engineer"

2. **Converse Enhanced Installation**:
   - Fixed in v0.1.6: Dependencies install directly via pip

3. **RAG-Anything Python Dependencies**:
   ```bash
   cd ~/mcp-servers/rag-anything-mcp
   pip install -r requirements.txt
   ```

4. **Database Permission Issues**:
   ```bash
   chmod 644 ~/mcp-servers/mcp-unified.db
   ```

## Uninstallation

Safe uninstall that preserves your existing MCPs:
```bash
python FEDERATED-INSTALLER-UNIFIED.py --uninstall
```

## Support

- **GitHub Issues**: [Report Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)
- **Latest Release**: [v0.1.7](https://github.com/justmy2satoshis/mcp-federation-core/releases)

## License

MIT License - See individual MCP repositories for specific licenses.

---

*MCP Federation Core v0.1.7 - 16 Unified MCPs for Claude Desktop*