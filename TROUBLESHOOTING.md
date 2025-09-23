# Troubleshooting Guide - MCP Federation Core

## Common Issues and Solutions

### 1. Python Package Installation Errors

#### Error: "error: externally-managed-environment"
This occurs with Python 3.11+ due to PEP 668 restrictions.

**Solution**: The installer now automatically handles this by adding `--break-system-packages` flag.

If you still have issues:

```powershell
# Option 1: Skip Python packages
.\installer.ps1 -SkipPython

# Option 2: Install manually with flag
python -m pip install mcp pydantic aiohttp numpy --break-system-packages

# Option 3: Use a virtual environment (recommended for development)
python -m venv mcp_env
.\mcp_env\Scripts\Activate.ps1
python -m pip install mcp pydantic aiohttp numpy
```

### 2. Antivirus / Windows Defender Blocking

#### Error: "ScriptContainedMaliciousContent"
Windows Defender may block direct script execution.

**Solution**: Use our two-step installation process:

```powershell
# Download first, then run locally
iwr -useb https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/setup.ps1 -OutFile setup.ps1
.\setup.ps1
```

### 3. PowerShell Execution Policy

#### Error: "Scripts are disabled on this system"

**Solution**: Set execution policy for current user:

```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

### 4. MCPs Not Appearing in Claude Desktop

**Common Causes**:
1. Claude Desktop needs restart
2. Configuration file syntax error
3. Path issues

**Solutions**:
```powershell
# 1. Fully quit Claude Desktop (check system tray)
# 2. Verify config file exists and is valid JSON
Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json

# 3. Reinstall with Force flag
.\installer.ps1 -Force
```

### 5. Database Initialization Errors

#### Error: "SQLITE_NOTADB" or database errors

**Solution**: Delete existing database and reinstall:

```powershell
Remove-Item "$HOME\mcp-servers\mcp-unified.db" -Force
.\installer.ps1
```

### 6. Ollama Installation Issues

#### Error: Ollama commands not recognized

**Solutions**:
```powershell
# Skip Ollama if not needed
.\installer.ps1 -SkipOllama

# Or install Ollama manually from:
# https://ollama.ai
```

### 7. Permission Denied Errors

**Solution**: Run PowerShell as Administrator:
1. Right-click PowerShell
2. Select "Run as Administrator"
3. Run installer

### 8. Incomplete Installation

If installation was interrupted:

```powershell
# Clean up and reinstall
.\uninstaller.ps1
.\installer.ps1 -Force
```

## Getting Help

If these solutions don't resolve your issue:

1. **Check existing issues**: https://github.com/justmy2satoshis/mcp-federation-core/issues
2. **Create new issue** with:
   - Error message
   - Python version: `python --version`
   - PowerShell version: `$PSVersionTable.PSVersion`
   - Windows version
   - Steps to reproduce

## Quick Diagnostics

Run this to gather diagnostic information:

```powershell
Write-Host "Python: $(python --version 2>&1)"
Write-Host "PowerShell: $($PSVersionTable.PSVersion)"
Write-Host "OS: $([System.Environment]::OSVersion.VersionString)"
Write-Host "Claude Config Exists: $(Test-Path "$env:APPDATA\Claude\claude_desktop_config.json")"
Write-Host "MCP Directory Exists: $(Test-Path "$HOME\mcp-servers")"
```