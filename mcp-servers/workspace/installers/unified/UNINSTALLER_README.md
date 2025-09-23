# MCP Federation Core - Safe Uninstaller

## Overview

The MCP Federation Core Safe Uninstaller is designed with **safety-first principles** to protect your existing MCP configurations while removing Federation components.

## Key Features

### 🛡️ Safety First Design
- **DEFAULT MODE**: Selective removal - ONLY removes Federation MCPs
- **Preserves**: Your existing MCPs, configurations, and non-Federation databases
- **Automatic Backups**: Creates timestamped backups before any modifications
- **Dry Run Mode**: Preview changes without making any modifications

## Uninstall Modes

### 1. Selective Uninstall (DEFAULT - RECOMMENDED)
Removes only MCP Federation components while preserving your existing MCPs.

```bash
# Windows
uninstall.bat selective

# Unix/Linux/macOS
./uninstall.sh selective
```

**What gets removed:**
- Federation MCPs only (kimi-k2, expert-role-prompt, etc.)
- Federation databases (mcp-unified.db, expert-roles.db, etc.)

**What gets preserved:**
- Your existing MCPs (filesystem, sqlite, etc.)
- Your custom configurations
- Non-Federation databases

### 2. Complete Uninstall (USE WITH CAUTION)
Removes ALL MCPs and configurations. Requires explicit confirmation.

```bash
# Windows
uninstall.bat complete

# Unix/Linux/macOS
./uninstall.sh complete
```

### 3. Dry Run Mode
Shows what would be removed without making any changes.

```bash
# Windows
uninstall.bat dry-run

# Unix/Linux/macOS
./uninstall.sh dry-run
```

### 4. Restore from Backup
Restores configurations from a previous uninstall backup.

```bash
# Windows
uninstall.bat restore

# Unix/Linux/macOS
./uninstall.sh restore
```

## Interactive Mode

Run without arguments for interactive menu:

```bash
# Windows
uninstall.bat

# Unix/Linux/macOS
./uninstall.sh
```

## Federation MCPs List

The following are considered Federation MCPs and will be removed in selective mode:

- `kimi-k2-code-context`
- `kimi-k2-heavy-processor`
- `kimi-k2-resilient`
- `expert-role-prompt`
- `converse-enhanced`
- `memory-graph`
- `rag-context-fixed`
- `sqlite-data-warehouse` (only if pointing to unified DB)
- `web-search-brave`
- `github-manager`
- `perplexity-sonar`
- `git-operations`
- `desktop-commander`
- `playwright-automation`
- `sequential-thinking`

## Backup System

### Automatic Backups
- Created before any modification
- Timestamped folders: `uninstaller_backups/YYYYMMDD_HHMMSS/`
- Contains all original configurations
- Includes manifest with metadata

### Backup Structure
```
uninstaller_backups/
└── 20241223_143022/
    ├── manifest.json
    ├── claude_desktop_backup.json
    ├── claude_code_backup.json
    └── zed_backup.json
```

### Restoring from Backup
```bash
# Interactive restore (choose from list)
uninstall.bat restore

# Restore specific backup
python uninstall.py --mode restore --backup-dir uninstaller_backups/20241223_143022
```

## Command-Line Options

```bash
python uninstall.py [options]

Options:
  --mode {selective,complete,restore,dry-run}
        Uninstall mode

  --mcp-base PATH
        Path to mcp_base directory

  --backup-dir PATH
        Specific backup directory for restore

  --force
        Skip confirmation prompts (dangerous!)
```

## Examples

### Testing Cycles
Perfect for development and testing cycles:

```bash
# 1. Test what would be removed
uninstall.bat dry-run

# 2. Remove Federation components only
uninstall.bat selective

# 3. Test your changes...

# 4. Reinstall Federation
python ../install.py

# 5. If something goes wrong, restore
uninstall.bat restore
```

### Complete Reset
For a full reset (removes everything):

```bash
# Windows
uninstall.bat complete --force

# Unix/Linux/macOS
./uninstall.sh complete --force
```

## Platform Support

### Windows
- Config: `%APPDATA%\Claude\claude_desktop_config.json`
- Script: `uninstall.bat`

### macOS
- Config: `~/Library/Application Support/Claude/claude_desktop_config.json`
- Script: `uninstall.sh`

### Linux
- Config: `~/.config/Claude/claude_desktop_config.json`
- Script: `uninstall.sh`

## Safety Features

1. **No Accidental Deletions**: Default mode preserves user MCPs
2. **Confirmation Required**: Complete uninstall requires typing "REMOVE ALL"
3. **Automatic Backups**: Every uninstall creates timestamped backups
4. **Dry Run Testing**: Preview changes before execution
5. **Selective Removal**: Granular control over what gets removed
6. **Platform Detection**: Automatically finds correct config paths

## Troubleshooting

### "No backups found"
- Check `uninstaller_backups/` directory exists
- Ensure you have run at least one uninstall

### "Config file not found"
- Verify Claude Desktop is installed
- Check platform-specific paths are correct

### "Permission denied"
- On Windows: Run as Administrator if needed
- On Unix: Use `sudo` if required

### Restore not working
- Verify backup directory exists
- Check manifest.json is present
- Ensure original config paths are accessible

## Development Use Cases

### Iterative Testing
```bash
# Install Federation
python install.py

# Test functionality...

# Remove Federation only
uninstall.bat selective

# Make changes...

# Reinstall
python install.py
```

### Clean Slate Testing
```bash
# Complete removal
uninstall.bat complete

# Fresh install
python install.py --setup-keys
```

## Important Notes

- **Default is SAFE**: Selective mode preserves your configurations
- **Backups are automatic**: Created before any changes
- **Test with dry-run**: Always preview changes first
- **Federation-only**: Designed specifically for MCP Federation Core

## Support

For issues:
1. Run `uninstall.bat dry-run` to diagnose
2. Check backups in `uninstaller_backups/`
3. Use restore mode if needed
4. Report issues with full output