# 🚀 MCP Federation Core v3.2

**The Ultimate Model Context Protocol Federation System** - 15 Integrated MCPs with Unified Database

[![Version](https://img.shields.io/badge/version-3.2-blue)](https://github.com/justmy2satoshis/mcp-federation-core)
[![MCPs](https://img.shields.io/badge/MCPs-15-green)](https://github.com/justmy2satoshis/mcp-federation-core)
[![License](https://img.shields.io/badge/license-MIT-purple)](LICENSE)

## ✨ Quick Installation

### Windows Installation (Two-Step Process)
Avoids antivirus blocking - Downloads first, then runs locally:

```powershell
# Step 1: Download setup script
iwr -useb https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/setup.ps1 -OutFile setup.ps1

# Step 2: Run setup (this will download and run the installer)
.\setup.ps1
```

**One-liner version:**
```powershell
iwr -useb https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/setup.ps1 -OutFile setup.ps1; .\setup.ps1
```

### macOS/Linux
```bash
curl -fsSL https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/install.sh | bash
```

### Alternative: Manual Installation
If the above methods are blocked:

```powershell
# Clone repository
git clone https://github.com/justmy2satoshis/mcp-federation-core.git
cd mcp-federation-core
.\installer.ps1
```

### Installation Options
```powershell
# Skip Python package installation (if you have pip issues)
.\installer.ps1 -SkipPython

# Skip Ollama installation
.\installer.ps1 -SkipOllama

# Force reinstall (overwrite existing)
.\installer.ps1 -Force

# Combine options as needed
.\installer.ps1 -SkipPython -SkipOllama
```

### 🤔 Which Installation Method Should I Use?

| Scenario | Recommended Method |
|----------|-------------------|
| First-time installation | Option 1: Standard (Regular PowerShell) |
| Personal computer | Option 1: Standard (Regular PowerShell) |
| Corporate/managed device | Option 2: Administrator |
| Permission errors with Option 1 | Option 2: Administrator |
| Updating existing installation | Option 1: Standard (Regular PowerShell) |

## 🗑️ Safe Uninstallation

Remove MCP Federation Core while preserving your personal MCPs:

### Windows
```powershell
irm https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/uninstaller.ps1 | iex
```

### macOS/Linux
```bash
curl -fsSL https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/uninstall.sh | bash
```

**Note**: This performs a selective uninstall, removing only Federation MCPs while preserving any other MCPs you have configured.

## ✅ Post-Installation

After installation completes:

1. **Restart Claude Desktop** to activate all MCPs
2. **Verify installation**: Check for 15 Federation MCPs in Claude settings
3. **Test functionality**: Try using `@expert-role-prompt` or `@sequential-thinking` in Claude

## 📋 What Gets Installed

The installer will:
- ✅ Configure 15 Federation MCPs in Claude Desktop
- ✅ Create unified database at `~/mcp-servers/mcp-unified.db`
- ✅ Set up API configurations (you'll be prompted for API keys)
- ✅ Initialize all MCP schemas and dependencies
- ✅ Preserve any existing personal MCPs you have configured

## 🔧 Troubleshooting

### Python Package Installation Errors (pip)
**For Python 3.11+ users**: The installer automatically handles the `--break-system-packages` requirement.

If you still see pip errors:
```powershell
# Option 1: Skip Python packages during installation
.\installer.ps1 -SkipPython

# Option 2: Install packages manually with the required flag
pip install mcp pydantic aiohttp numpy --break-system-packages
```

### "Malicious Content" or Antivirus Blocking
- Use the two-step process above (downloads first, runs locally)
- Or download setup.ps1 manually from GitHub and run locally
- Add an exception for the mcp-federation-core folder in Windows Defender

### "Scripts are disabled on this system" Error
```powershell
# Run this first, then try installation again:
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### "Access denied" or Permission Errors
- Run PowerShell as Administrator
- Ensure antivirus isn't blocking the script

### Some MCPs Not Appearing in Claude
- Fully quit Claude Desktop (check system tray)
- Restart Claude Desktop
- Check the config file manually: `%APPDATA%\Claude\claude_desktop_config.json`

### Database Initialization Errors
- Delete `~/mcp-servers/mcp-unified.db` if it exists
- Run the installer again

For more help, see [Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)

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