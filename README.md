# 🚀 MCP Federation Core v3.2

**The Ultimate Model Context Protocol Federation System** - 15 Integrated MCPs with Unified Database

[![Version](https://img.shields.io/badge/version-3.2-blue)](https://github.com/justmy2satoshis/mcp-federation-core)
[![MCPs](https://img.shields.io/badge/MCPs-15-green)](https://github.com/justmy2satoshis/mcp-federation-core)
[![License](https://img.shields.io/badge/license-MIT-purple)](LICENSE)

## ✨ One-Line Installation

### Windows (PowerShell as Admin):
```powershell
irm https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installer-safe.ps1 | iex
```

### macOS/Linux:
```bash
curl -fsSL https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/install.sh | bash
```

## 🗑️ Safe Uninstallation

**Remove ONLY Federation MCPs** (preserves your other MCPs):

### Windows:
```powershell
cd ~/mcp-servers/installers/unified
./uninstall.bat selective
```

### macOS/Linux:
```bash
cd ~/mcp-servers/installers/unified
./uninstall.sh selective
```

## 🎯 What's New in v3.2

- ✅ **Fixed**: SQLite database path issues (no more SQLITE_NOTADB errors)
- ✅ **Fixed**: Dynamic path resolution (no placeholders)
- ✅ **New**: Safe selective uninstaller
- ✅ **New**: Automatic database schema initialization
- ✅ **New**: API key configuration wizard
- ✅ **Improved**: Cross-platform compatibility
- ✅ **Verified**: All 15 MCPs working together

## 📦 What You Get

### 15 Production-Ready MCPs:
1. **sqlite** - Unified database operations
2. **expert-role-prompt** - 50 AI expert roles with reasoning
3. **kimi-k2-resilient-enhanced** - Resilient data storage
4. **kimi-k2-code-context-enhanced** - Code analysis with vector search
5. **rag-context** - RAG-based context management
6. **converse** - Multi-model AI consensus (Ollama auto-detect!)
7. **web-search** - Brave search integration
8. **github-manager** - GitHub repository management
9. **memory** - Knowledge graph storage
10. **filesystem** - File system operations
11. **desktop-commander** - System commands
12. **perplexity** - AI-powered search
13. **playwright** - Browser automation
14. **git-ops** - Git version control
15. **sequential-thinking** - Advanced problem solving

## 🔑 API Keys Required

The installer will guide you through API key setup. You'll need:

### Required:
- **Brave Search**: [Get free API key](https://api.search.brave.com/app/keys)
- **Perplexity**: [Get API key](https://www.perplexity.ai/settings/api)

### Optional (for enhanced features):
- **OpenAI**: For GPT models
- **Moonshot (Kimi)**: For Kimi K2 features
- **xAI**: For Grok models
- **Cohere**: For Cohere models
- **OpenRouter**: For model routing
- **GitHub**: For repository management

## 💻 System Requirements

### Minimum:
- RAM: 4GB
- Storage: 500MB
- Node.js 18+
- Python 3.8+

### Recommended:
- RAM: 8GB
- Storage: 1GB
- Stable internet connection

## 🛠️ Troubleshooting

### Common Issues:

**SQLITE_NOTADB Error**
- ✅ Fixed in v3.2 - run uninstaller then reinstall

**MCPs Not Showing in Claude**
- Restart Claude Desktop after installation
- Check `%APPDATA%\Claude\claude_desktop_config.json` has all 15 MCPs

**Installation Fails**
- Run PowerShell as Administrator
- Ensure Node.js and Python are installed
- Check firewall isn't blocking npm/pip

**See [TROUBLESHOOTING.md](TROUBLESHOOTING.md) for detailed solutions**

## 🧪 Testing

Verify your installation:
```bash
# Test database connectivity
python ~/mcp-servers/installers/unified/test_installation.py

# Test complete cycle
python ~/mcp-servers/installers/unified/test_complete_cycle.py
```

## 📚 Documentation

- [Installation Guide](docs/INSTALLATION.md)
- [Uninstaller Guide](installers/unified/UNINSTALLER_README.md)
- [API Key Setup](docs/API_SETUP.md)
- [Troubleshooting](TROUBLESHOOTING.md)
- [Testing Guide](docs/TESTING.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## 🚀 Quick Start

1. **Install**: Run the one-liner above
2. **Configure**: Enter API keys when prompted
3. **Restart**: Close and reopen Claude Desktop
4. **Test**: Try `@sqlite` or `@expert-role-prompt` in Claude

## 🤝 Contributing

We welcome contributions! See [CONTRIBUTING.md](CONTRIBUTING.md)

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🌟 Support

- **Issues**: [GitHub Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)
- **Discussions**: [GitHub Discussions](https://github.com/justmy2satoshis/mcp-federation-core/discussions)

---

**Built with ❤️ for the Claude community**