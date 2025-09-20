# MCP Federation Core 🧠
> Lightweight Model Context Protocol Federation System - Connect Your AI Context

[![Version](https://img.shields.io/badge/version-2.0.0-blue.svg)](https://github.com/justmy2satoshis/mcp-federation-core)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![MCPs](https://img.shields.io/badge/MCPs-15-orange.svg)](mcp-servers)
[![Database](https://img.shields.io/badge/database-unified-purple.svg)](mcp-unified.db)

## 🎯 What is MCP Federation Core?

MCP Federation Core is a lightweight, unified database system that enables seamless communication between 15 different Model Context Protocol servers. It provides a foundational framework for AI context management, allowing MCPs to share data, persist information, and collaborate through a federated architecture.

### Key Features:
- 🔄 **Unified Database**: Single SQLite database shared across all MCPs
- 🌐 **Cross-MCP Communication**: Query data from any MCP using `from_mcp` parameter
- ⚡ **Lightweight**: Optimized for standard hardware (4GB RAM minimum)
- 🛠️ **Expert Role System**: 50 specialized AI expert roles with confidence scoring
- 🧠 **Advanced Reasoning**: Chain-of-Thought (CoT) and Tree-of-Thoughts (ToT) frameworks
- 🔌 **REST API**: External integration via port 3456
- 📦 **Easy Installation**: One-command setup with PowerShell installer

## 📊 System Requirements

### Minimum Requirements:
- **RAM**: 4GB
- **Storage**: 500MB free space
- **CPU**: Dual-core 2.0GHz
- **OS**: Windows 10/11, macOS 10.15+, Linux (Ubuntu 20.04+)
- **Runtime**: Node.js 18+, Python 3.8+

### Recommended:
- **RAM**: 8GB
- **Storage**: 1GB free space  
- **CPU**: Quad-core 2.5GHz
- **Network**: Stable internet for web-based MCPs

## 🚀 Quick Start

### 1. Clone the repository:
```bash
git clone https://github.com/justmy2satoshis/mcp-federation-core.git
cd mcp-federation-core
```

### 2. Run the installer:
```powershell
# Windows
.\install-mcp-suite.ps1

# macOS/Linux (coming soon)
chmod +x install-mcp-suite.sh
./install-mcp-suite.sh
```

### 3. Configure Claude Desktop:
The installer automatically updates your Claude Desktop configuration. Restart Claude Desktop to activate all MCPs.

## 📦 Included MCPs (15 Total)

### Custom MCPs (3):
1. **expert-role-prompt** (v2.0) - 50 expert roles with reasoning frameworks
2. **kimi-k2-resilient-enhanced** - Resilient data storage with circuit breakers  
3. **kimi-k2-code-context-enhanced** - Code analysis with vector search

### Standard MCPs (12):
4. **sequential-thinking** - Step-by-step problem solving with branching
5. **memory** - Persistent knowledge graph storage
6. **filesystem** - File system operations and management
7. **web-search** - Brave search API integration
8. **sqlite** - Direct SQLite database operations
9. **perplexity** - AI-powered search and answers
10. **desktop-commander** - System command execution
11. **playwright** - Browser automation and web scraping
12. **github-manager** - GitHub repository management
13. **git-ops** - Git version control operations
14. **rag-context** - RAG-based context management
15. **converse** - Multi-model AI consensus

## 🔬 Performance Benchmarks

Results from load testing on standard hardware (32 cores, 61GB RAM):

### Response Times:
- **Database Write**: 5.67ms average
- **Database Read**: 0.03ms average  
- **Cross-MCP Query**: 0.03ms average
- **MCP Startup**: ~500ms per MCP

### Resource Usage:
- **Idle Memory**: 21MB
- **Active Memory**: 200-400MB
- **CPU (idle)**: 0.4%
- **CPU (active)**: 15-25%
- **Database Size**: 16KB (grows with usage)

### Concurrent Operations:
- **Max Parallel MCPs**: 15 (all running)
- **Requests/Second**: 50+ sustained

## 🏗️ Architecture

### Unified Database Schema:
```sql
CREATE TABLE context (
    id TEXT PRIMARY KEY,
    mcp_source TEXT NOT NULL,
    data TEXT NOT NULL,
    metadata TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expires_at TIMESTAMP,
    ttl INTEGER
);
```

### Cross-MCP Communication:
```python
# Store data from one MCP
store_context(key="analysis_result", data=result, mcp_source="code-context")

# Retrieve from another MCP
data = retrieve_context(key="analysis_result", from_mcp="code-context")

# Query across all MCPs
all_data = retrieve_context(key="*", from_mcp="*")
```

## 🧪 Testing

Run the included test suite to verify your installation:

```bash
# Test cross-MCP communication
python test_mcp_persistence.py

# Check database connectivity
python check_mcp_db.py

# Run performance benchmark
python benchmark_mcp_performance.py
```

## 🛠️ Configuration

### Claude Desktop Integration:
The installer automatically configures Claude Desktop. Manual configuration can be done by editing:
- Windows: `%APPDATA%\Claude\claude_desktop_config.json`
- macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Linux: `~/.config/Claude/claude_desktop_config.json`

### REST API Access:
The expert-role-prompt MCP includes a REST API server:
```bash
# Start REST API server (port 3456)
node mcp-servers/expert-role-prompt/rest-api-server.js

# Example API call
curl http://localhost:3456/api/nominate-expert \
  -H "Content-Type: application/json" \
  -d '{"task": "analyze Python code"}'
```

## 📚 Documentation

### Expert Roles (50 Available):
- Software Engineers (Frontend, Backend, Full-Stack)
- AI/ML Specialists (Data Scientists, ML Engineers)
- DevOps & Infrastructure (Cloud, Security, SRE)
- Product & Design (PM, UX, UI)
- Business & Strategy (Analyst, Consultant)
- And 40+ more specialized roles

### Reasoning Frameworks:
- **Chain-of-Thought (CoT)**: Step-by-step logical reasoning
- **Tree-of-Thoughts (ToT)**: Branching exploration of solutions
- **Confidence Scoring**: 0-100% match with rationale

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

### Development Setup:
```bash
# Clone with submodules
git clone --recursive https://github.com/justmy2satoshis/mcp-federation-core.git

# Install dev dependencies
npm install --dev
pip install -r requirements-dev.txt

# Run tests
npm test
pytest tests/
```

## 📄 License

MIT License - see [LICENSE](LICENSE) file for details.

## 🔗 Related Projects

- [expert-role-prompt](https://github.com/justmy2satoshis/expert-role-prompt) - Standalone expert role MCP
- [Claude Desktop](https://claude.ai/download) - Required for MCP integration
- [MCP Specification](https://modelcontextprotocol.io) - Official MCP documentation

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/justmy2satoshis/mcp-federation-core/discussions)
- **Email**: notyourbuddyfriend2@protonmail.com

## 🚀 Roadmap

### Current Version (2.0.0 - Basic):
- ✅ 15 MCPs with unified database
- ✅ Cross-MCP communication
- ✅ Expert role system
- ✅ REST API integration

### Coming Soon (3.0.0 - Pro):
- 🔄 30+ MCPs including advanced AI/ML
- 🔄 Web dashboard for monitoring
- 🔄 Enterprise authentication (OAuth, SAML)
- 🔄 Cloud synchronization
- 🔄 Advanced workflow automation
- 🔄 GPU acceleration support

---

**Built with ❤️ by justmy2satoshis**
