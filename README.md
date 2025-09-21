# MCP Enterprise Suite
## Unified MCP Repository for Claude Desktop & Claude Code CLI

[![MCPs](https://img.shields.io/badge/MCPs-15-blue)](./mcps)
[![License](https://img.shields.io/badge/License-MIT-green)](./LICENSE)
[![Platform](https://img.shields.io/badge/Platform-Windows%20|%20MacOS%20|%20Linux-lightgrey)]()

A comprehensive, production-ready collection of Model Context Protocol (MCP) servers for both Claude Desktop and Claude Code CLI environments. This unified repository provides seamless integration, automated installation, and consistent configuration across both platforms.

## ✅ Included MCPs (15 Core)

| MCP | Description | Runtime | Status |
|-----|-------------|---------|--------|
| **expert-role-prompt** | Expert role nomination and task-specific prompting | Node.js | ✅ Active |
| **kimi-k2-resilient** | Resilient enhanced Kimi K2 implementation | Python | ✅ Active |
| **kimi-k2-code-context** | Code context management with enhanced features | Python | ✅ Active |
| **filesystem** | File system access and operations | NPX | ✅ Active |
| **memory** | Knowledge graph and memory management | NPX | ✅ Active |
| **sequential-thinking** | Sequential reasoning and thought chains | NPX | ✅ Active |
| **desktop-commander** | Desktop automation and control | NPX | ✅ Active |
| **perplexity** | Perplexity AI search integration | NPX | ✅ Active |
| **converse** | Multi-model AI conversation (OpenAI, Gemini) | NPX | ✅ Active |
| **rag-context** | RAG memory and context management | NPX | ✅ Active |
| **playwright** | Browser automation and web scraping | NPX | ✅ Active |
| **sqlite** | SQLite database operations | NPX | ✅ Active |
| **git-ops** | Git repository operations | NPX | ✅ Active |
| **github-manager** | GitHub API integration | NPX | ✅ Active |
| **web-search** | Brave search API integration | NPX | ✅ Active |

## 🚀 Quick Start

### Prerequisites
- Node.js 18+ and npm
- Python 3.8+
- Claude Desktop and/or Claude Code CLI
- Git

### Installation

```powershell
# Clone repository
git clone https://github.com/yourusername/mcp-enterprise-suite
cd mcp-enterprise-suite

# Copy and configure environment variables
copy .env.template .env
# Edit .env with your API keys

# Run unified installer (auto-detects environment)
.\scripts\installation\install.ps1 -Environment auto

# Or specify environment explicitly
.\scripts\installation\install.ps1 -Environment desktop  # For Claude Desktop only
.\scripts\installation\install.ps1 -Environment code     # For Claude Code CLI only
.\scripts\installation\install.ps1 -Environment both     # For both environments
```

### Verification

```powershell
# Validate installation
.\scripts\installation\validate-installation.ps1

# For Claude Code CLI users
claude mcp list

# For Claude Desktop users
# Check the UI for connected MCPs
```

## 📁 Repository Structure

```
mcp-enterprise-suite/
├── mcps/                      # All MCP servers (shared binaries)
│   ├── expert-role-prompt/
│   ├── kimi-k2-resilient-enhanced/
│   ├── kimi-k2-code-context-enhanced/
│   └── ...
├── configs/                   # Configuration files
│   ├── claude-desktop/       # Desktop-specific configs
│   ├── claude-code/          # CLI-specific configs
│   ├── shared/               # Shared configurations
│   └── templates/            # Configuration templates
├── scripts/                   # Automation scripts
│   ├── installation/         # Installation scripts
│   └── validation/           # Validation scripts
├── databases/                 # Database storage
│   ├── sqlite/               # SQLite databases
│   ├── metadata/             # Metadata storage
│   └── configs/              # Database configurations
├── docs/                      # Documentation
│   ├── setup/                # Setup guides
│   └── mcps/                 # MCP-specific documentation
├── tests/                     # Test suites
├── .env.template             # Environment variable template
└── README.md                 # This file
```

## 🔧 Configuration

### Environment Variables
Create a `.env` file from `.env.template`:

```bash
# API Keys
OPENAI_API_KEY=your_key_here
PERPLEXITY_API_KEY=your_key_here
GITHUB_PERSONAL_ACCESS_TOKEN=your_token_here
BRAVE_API_KEY=your_key_here

# Paths (customize as needed)
SQLITE_PATH=./databases/sqlite/
RAG_DATA_DIR=./ClaudeRAG/data
```

### Claude Desktop Configuration
The installer automatically configures Claude Desktop. Manual configuration files are in:
- `configs/templates/claude-desktop-config.template.json`
- Location: `%APPDATA%\Claude\claude_desktop_config.json`

### Claude Code CLI Configuration
The installer uses `claude mcp add` commands. Manual configuration:
- `configs/templates/claude-code-config.template.json`
- Location: `%USERPROFILE%\.claude.json`

## 📊 Supported Databases

- **SQLite** - Lightweight local storage (current)
- **PostgreSQL** - Scalable relational database (coming soon)
- **Redis** - In-memory data structure store (coming soon)
- **MongoDB** - Document-oriented database (coming soon)

## 🛠️ Advanced Usage

### Custom MCP Installation
```powershell
# Add a custom MCP to Claude Code
claude mcp add custom-mcp node "path/to/custom-mcp/server.js"

# Add with environment variables
claude mcp add custom-mcp node "path/to/server.js" -e API_KEY=your_key
```

### Debugging MCPs
```powershell
# Check MCP logs
claude mcp logs [mcp-name]

# Restart specific MCP
claude mcp restart [mcp-name]

# Test MCP function
claude mcp invoke [mcp-name] [function] '{\"args\":\"value\"}'
```

## 🎯 Roadmap

### Core Features
- [x] 15 Core MCPs integrated
- [x] Unified repository structure
- [x] Automated installation scripts
- [x] Environment auto-detection
- [x] Comprehensive documentation

### Priority 1 - New MCPs (Coming Soon)
- [ ] Ollama - Local LLM integration
- [ ] Docker - Container management
- [ ] Terraform - Infrastructure as Code
- [ ] Linear - Project management
- [ ] Notion - Knowledge base integration
- [ ] Airtable - Database operations
- [ ] Vercel - Deployment automation

### Priority 2 - Enhanced Features
- [ ] Betterstack - Monitoring and logging
- [ ] Kubernetes/K3s - Container orchestration
- [ ] Web UI for MCP management
- [ ] Cross-platform GUI installer
- [ ] MCP marketplace integration

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](./docs/CONTRIBUTING.md) for guidelines.

### Development Setup
```bash
# Fork and clone
git clone https://github.com/yourusername/mcp-enterprise-suite
cd mcp-enterprise-suite

# Create feature branch
git checkout -b feature/your-feature

# Make changes and test
.\scripts\installation\validate-installation.ps1

# Submit PR
```

## 📝 License

This project is licensed under the MIT License - see [LICENSE](./LICENSE) file for details.

## 🔗 Resources

- [MCP Specification](https://github.com/anthropics/mcp)
- [Claude Desktop](https://claude.ai/desktop)
- [Claude Code CLI](https://github.com/anthropics/claude-code)
- [Setup Guide](./docs/setup/SETUP_GUIDE.md)
- [API Documentation](./docs/mcps/MCP_REFERENCE.md)

## 💬 Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/mcp-enterprise-suite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/mcp-enterprise-suite/discussions)
- **Email**: support@your-domain.com

## 🙏 Acknowledgments

Special thanks to:
- Anthropic for creating the MCP specification
- All MCP package authors and contributors
- The Claude community for feedback and testing

---

**Note**: Replace `yourusername` with your actual GitHub username when setting up the repository.