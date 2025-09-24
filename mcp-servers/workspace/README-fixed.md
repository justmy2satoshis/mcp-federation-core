# 🚀 MCP Federation Core v3.2.2 FIXED

**The Ultimate Model Context Protocol Federation System** - 15 Integrated MCPs with Unified Database

[![Version](https://img.shields.io/badge/version-3.2.2_FIXED-blue)](https://github.com/justmy2satoshis/mcp-federation-core)
[![MCPs](https://img.shields.io/badge/MCPs-15-green)](https://github.com/justmy2satoshis/mcp-federation-core)
[![License](https://img.shields.io/badge/license-MIT-purple)](LICENSE)

## ⚠️ CRITICAL FIX NOTICE

**The original installer (v3.2.1) does NOT actually configure MCPs!** It only prints success messages without doing the work. Use the fixed version below.

## ✨ Quick Installation

### Windows Installation - FIXED VERSION

**Step 1: Download the setup script**
```powershell
iwr -useb https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/setup.ps1 -OutFile setup.ps1
```

**Step 2: Run the setup script**
```powershell
.\setup.ps1
```

> **Note**: These commands should be run SEPARATELY, not on the same line with semicolon.

### Alternative: Direct Fixed Installer Download

If you want to use the fixed installer directly:

```powershell
# Download the FIXED installer
iwr -useb https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installer-fixed.ps1 -OutFile installer-fixed.ps1

# Run the fixed installer
.\installer-fixed.ps1
```

### Verify Installation Actually Worked

**IMPORTANT**: After installation, verify MCPs were actually configured:

```powershell
# Download verification script
iwr -useb https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/verify-installation.ps1 -OutFile verify-installation.ps1

# Run verification
.\verify-installation.ps1
```

Expected output:
- ✅ Configuration file exists
- ✅ Valid JSON configuration
- ✅ Found 15+ configured MCPs
- ✅ All 15 Federation MCPs are configured

If you see "❌ FAILED: No MCPs configured", the installer didn't work!

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

# Use the FIXED installer
.\installer-fixed.ps1
```

### Installation Options
```powershell
# Skip Python package installation (if you have pip issues)
.\installer-fixed.ps1 -SkipPython

# Skip Ollama installation
.\installer-fixed.ps1 -SkipOllama

# Force reinstall (overwrite existing)
.\installer-fixed.ps1 -Force

# Test without making changes
.\installer-fixed.ps1 -WhatIf
```

## 🤔 Which Installation Method Should I Use?

| Scenario | Recommended Method |
|----------|-------------------|
| Fresh installation | Use installer-fixed.ps1 |
| Existing failed installation | Use installer-fixed.ps1 -Force |
| Want to verify first | Run verify-installation.ps1 |
| Having issues | Check analysis-report.md for details |

## 🗑️ Safe Uninstallation

Remove MCP Federation Core while preserving your personal MCPs:

### Windows
```powershell
cd ~/mcp-servers/installers/unified
.\uninstall.bat selective
```

### macOS/Linux
```bash
cd ~/mcp-servers/installers/unified
./uninstall.sh selective
```

## ✅ Post-Installation

After installation completes:

1. **Run verification script** to ensure MCPs are actually configured
2. **Restart Claude Desktop** to activate all MCPs
3. **Check Claude settings** for 15 Federation MCPs
4. **Test functionality**: Try using `@expert-role-prompt` or `@sequential-thinking` in Claude

## 📋 What Gets Installed

The installer will:
- ✅ **ACTUALLY** Configure 15 Federation MCPs in Claude Desktop (fixed version)
- ✅ Create unified database at `~/mcp-servers/mcp-unified.db`
- ✅ Set up API configurations (you'll be prompted for API keys)
- ✅ Initialize all MCP schemas and dependencies
- ✅ Preserve any existing personal MCPs you have configured

## 🔧 Troubleshooting

### MCPs Not Showing After Installation

**Most likely cause**: You used installer.ps1 instead of installer-fixed.ps1

1. Run `verify-installation.ps1` to check
2. If it shows "No MCPs configured", run:
   ```powershell
   .\installer-fixed.ps1 -Force
   ```

### Python Package Installation Errors (pip)
**For Python 3.11+ users**: The installer automatically handles the `--break-system-packages` requirement.

If you still see pip errors:
```powershell
# Option 1: Skip Python packages during installation
.\installer-fixed.ps1 -SkipPython

# Option 2: Install packages manually with the required flag
python -m pip install mcp pydantic aiohttp numpy --break-system-packages
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

## 🎯 What's Fixed in v3.2.2

- ✅ **FIXED**: Installer now ACTUALLY configures MCPs (not just prints messages)
- ✅ **FIXED**: Configuration is saved to claude_desktop_config.json
- ✅ **FIXED**: Verification confirms MCPs are configured
- ✅ **FIXED**: Accurate success/failure reporting
- ✅ **FIXED**: Python 3.11+ compatibility with --break-system-packages
- ✅ **FIXED**: NativeCommandError with python -m pip

## 📦 What You Get

### 15 Production-Ready MCPs (When Using Fixed Installer):
1. **sqlite** - Unified database operations
2. **expert-role-prompt** - 50 AI expert roles with reasoning
3. **kimi-k2-resilient-enhanced** - Resilient data storage
4. **kimi-k2-code-context-enhanced** - Code analysis with vector search
5. **rag-context** - RAG-based context management
6. **converse** - Multi-model AI consensus
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
- **GitHub**: For repository management
- Other provider keys as needed

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

## 🧪 Testing

Verify your installation:
```powershell
# Run the verification script
.\verify-installation.ps1

# Check configuration manually
$config = Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json
$config.mcpServers.PSObject.Properties.Name.Count  # Should be 15 or more
```

## 📚 Documentation

- [Installation Analysis](analysis-report.md) - Why the original installer doesn't work
- [Troubleshooting](TROUBLESHOOTING.md)
- [Contributing](CONTRIBUTING.md)
- [Changelog](CHANGELOG.md)

## 🤝 Contributing

We welcome contributions! Please test your changes with verify-installation.ps1

## 📝 License

MIT License - see [LICENSE](LICENSE)

## 🌟 Support

- **Issues**: [GitHub Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)
- **Critical Bug**: Original installer doesn't configure MCPs - use installer-fixed.ps1

---

**Built with ❤️ for the Claude community - Now actually works!**