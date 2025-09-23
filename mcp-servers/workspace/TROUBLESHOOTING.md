# Troubleshooting Guide

## Common Issues and Solutions

### 1. SQLITE_NOTADB Error

**Symptoms**: Error message about database not being valid SQLite

**Cause**: Old installation pointing to wrong database path

**Solution**:
```powershell
# 1. Uninstall completely
cd ~/mcp-servers/installers/unified
./uninstall.bat selective

# 2. Fresh install
irm https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installer-safe.ps1 | iex
```

### 2. MCPs Not Showing in Claude Desktop

**Symptoms**: Installed but MCPs don't appear in Claude

**Solutions**:
1. **Restart Claude Desktop** - Close completely and reopen
2. **Check config file**:
   ```powershell
   notepad %APPDATA%\Claude\claude_desktop_config.json
   ```
   Should contain 15 mcpServers entries

3. **Verify Node.js/Python**:
   ```powershell
   node --version  # Should be 18+
   python --version  # Should be 3.8+
   ```

### 3. Installation Fails

**PowerShell Execution Policy**:
```powershell
# Run as Administrator
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**Network Issues**:
- Check firewall settings
- Verify npm/pip can access internet
- Try using a VPN if blocked

### 4. API Keys Not Working

**Validation Failed**:
- Double-check key copied correctly (no spaces)
- Verify key is active on provider's dashboard
- Some keys take time to activate

**Missing .env File**:
```powershell
# Check if .env exists
dir $HOME\mcp-servers\.env
```

### 5. Uninstaller Issues

**Not Finding All 15 MCPs**:
- Update to latest version
- Run dry-run first to see what will be removed:
  ```powershell
  cd ~/mcp-servers/installers/unified
  ./uninstall.bat dry-run
  ```

**Want Complete Removal**:
- Choose option 2 but requires typing 'REMOVE ALL'
- This removes ALL MCPs, not just Federation

### 6. Database Errors

**Check Database**:
```powershell
# Verify database exists and has correct size
dir $HOME\mcp-servers\mcp_base\databases\mcp-unified.db
# Should be > 16KB
```

**Reinitialize Database**:
```powershell
python $HOME\mcp-servers\installers\unified\db_manager.py
```

### 7. Performance Issues

**High Memory Usage**:
- Normal: 200-400MB active
- Check for runaway processes
- Restart Claude Desktop

**Slow Response**:
- Check internet connection for web-based MCPs
- Verify CPU not overloaded
- Consider closing some MCPs if on minimum specs

## Getting Help

1. **Check Logs**:
   ```powershell
   # Installation log
   type $HOME\mcp-servers\install.log

   # Validation report
   type $HOME\mcp-servers\mcp_base\validation_report.txt
   ```

2. **Run Validation**:
   ```powershell
   python $HOME\mcp-servers\installers\unified\validator.py
   ```

3. **Create Issue**:
   - Go to [GitHub Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)
   - Include validation report
   - Specify OS and Claude version

## Emergency Recovery

If everything is broken:

1. **Manual Cleanup**:
   ```powershell
   # Remove Federation from Claude config manually
   notepad %APPDATA%\Claude\claude_desktop_config.json
   # Delete the 15 Federation MCP entries
   ```

2. **Delete Federation Directory**:
   ```powershell
   rmdir /s $HOME\mcp-servers\mcp_base
   ```

3. **Fresh Start**:
   ```powershell
   # Reinstall from scratch
   irm https://raw.githubusercontent.com/justmy2satoshis/mcp-federation-core/main/installer-safe.ps1 | iex
   ```

## Platform-Specific Issues

### Windows
- Run PowerShell as Administrator
- Check Windows Defender not blocking
- Ensure .NET Framework updated

### macOS
- Grant terminal full disk access
- Check Gatekeeper settings
- Use `sudo` if permission denied

### Linux
- Ensure proper permissions on home directory
- Check SELinux/AppArmor policies
- Install build-essential if compilation fails

## MCP-Specific Troubleshooting

### SQLite MCP
- Ensure database path is absolute
- Check file permissions
- Verify database not locked

### Converse MCP
- Ollama auto-detection requires Ollama running
- API keys needed if Ollama not available
- Check model names are correct

### Web Search MCP
- Brave API key required (free)
- Check rate limits not exceeded
- Verify network connectivity

### Expert Role Prompt
- Large initial load is normal (50 roles)
- Caching improves performance over time

## Error Messages

### "Cannot find module"
- Run `npm install` in the MCP directory
- Check Node.js version compatibility

### "Permission denied"
- Windows: Run as Administrator
- Unix: Use sudo or check file ownership

### "ECONNREFUSED"
- Service not running
- Port blocked by firewall
- Wrong port configuration

### "Rate limit exceeded"
- API quota exhausted
- Add delays between requests
- Check provider dashboard

## Still Need Help?

1. **Check existing issues**: [GitHub Issues](https://github.com/justmy2satoshis/mcp-federation-core/issues)
2. **Join discussion**: [GitHub Discussions](https://github.com/justmy2satoshis/mcp-federation-core/discussions)
3. **Review docs**: [Full Documentation](docs/)

Remember to include:
- OS and version
- Claude Desktop version
- Error messages (full text)
- Validation report output