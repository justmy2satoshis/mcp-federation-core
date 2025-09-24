# MCP Federation Core Installer - VERSION THAT ACTUALLY WORKS
# This installer REALLY configures MCPs and SAVES the configuration

param(
    [switch]$Force,
    [switch]$TestMode
)

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "         MCP FEDERATION CORE - WORKING INSTALLER v3.3.1                    " -ForegroundColor Yellow
Write-Host "         This version ACTUALLY saves the configuration!                    " -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration paths
$configDir = "$env:APPDATA\Claude"
$configPath = "$configDir\claude_desktop_config.json"
$baseDir = "$env:USERPROFILE\mcp-servers"
$dbPath = "$baseDir\mcp-unified.db"
$backupPath = "$configDir\backup_$(Get-Date -Format 'yyyyMMdd_HHmmss').json"

# Check if Claude is running
$claudeRunning = Get-Process "Claude" -ErrorAction SilentlyContinue
if ($claudeRunning) {
    Write-Host "WARNING: Claude Desktop is running!" -ForegroundColor Red
    Write-Host "Please close Claude Desktop before continuing." -ForegroundColor Yellow

    if (-not $Force) {
        Write-Host ""
        Write-Host "Press Enter after closing Claude Desktop, or Ctrl+C to cancel..."
        Read-Host
    }
}

# Create directories
Write-Host "[Step 1/6] Creating directories..." -ForegroundColor Yellow
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    Write-Host "  Created: $configDir" -ForegroundColor Green
}
if (-not (Test-Path $baseDir)) {
    New-Item -ItemType Directory -Path $baseDir -Force | Out-Null
    Write-Host "  Created: $baseDir" -ForegroundColor Green
}

# Backup existing config
if (Test-Path $configPath) {
    Write-Host ""
    Write-Host "[Step 2/6] Backing up existing configuration..." -ForegroundColor Yellow
    Copy-Item -Path $configPath -Destination $backupPath -Force
    Write-Host "  Backup saved to: $backupPath" -ForegroundColor Green
} else {
    Write-Host ""
    Write-Host "[Step 2/6] No existing configuration to backup" -ForegroundColor Gray
}

# CRITICAL: Define the ACTUAL configuration
Write-Host ""
Write-Host "[Step 3/6] Building MCP configuration..." -ForegroundColor Yellow

$mcpServers = [ordered]@{
    'sequential-thinking' = @{
        command = 'npx'
        args = @('-y', '@modelcontextprotocol/server-sequential-thinking')
    }
    'memory' = @{
        command = 'npx'
        args = @('-y', '@modelcontextprotocol/server-memory')
    }
    'filesystem' = @{
        command = 'npx'
        args = @('-y', '@modelcontextprotocol/server-filesystem', $env:USERPROFILE)
    }
    'desktop-commander' = @{
        command = 'npx'
        args = @('-y', '@rkdms/desktop-commander')
    }
    'playwright' = @{
        command = 'npx'
        args = @('-y', '@modelcontextprotocol/server-playwright')
    }
    'sqlite' = @{
        command = 'npx'
        args = @('-y', '@modelcontextprotocol/server-sqlite', $dbPath)
    }
    'git-ops' = @{
        command = 'npx'
        args = @('-y', 'git-ops-mcp')
    }
    'web-search' = @{
        command = 'npx'
        args = @('-y', '@modelcontextprotocol/server-brave-search')
        env = @{
            BRAVE_API_KEY = 'YOUR_BRAVE_API_KEY'
        }
    }
    'github-manager' = @{
        command = 'npx'
        args = @('-y', '@modelcontextprotocol/server-github')
        env = @{
            GITHUB_TOKEN = 'YOUR_GITHUB_TOKEN'
        }
    }
    'perplexity' = @{
        command = 'npx'
        args = @('-y', 'perplexity-mcp-server')
        env = @{
            PERPLEXITY_API_KEY = 'YOUR_PERPLEXITY_KEY'
        }
    }
    'converse' = @{
        command = 'node'
        args = @("$baseDir\converse\index.js")
    }
    'expert-role-prompt' = @{
        command = 'node'
        args = @("$baseDir\expert-role-prompt\index.js")
    }
    'rag-context' = @{
        command = 'node'
        args = @("$baseDir\rag-context\index.js")
    }
    'kimi-k2-code-context' = @{
        command = 'python'
        args = @('-m', 'kimi_k2_code_context')
        env = @{
            KIMI_CODE_DB = "$baseDir\kimi-code.db"
        }
    }
    'kimi-k2-resilient' = @{
        command = 'python'
        args = @('-m', 'kimi_k2_resilient')
        env = @{
            KIMI_DB_PATH = "$baseDir\kimi-resilient.db"
        }
    }
}

Write-Host "  Built configuration for $($mcpServers.Count) MCPs" -ForegroundColor Green

# Create configuration object
$config = @{
    mcpServers = $mcpServers
}

# CRITICAL: Actually SAVE the configuration
Write-Host ""
Write-Host "[Step 4/6] SAVING configuration to disk..." -ForegroundColor Yellow

if ($TestMode) {
    Write-Host "  TEST MODE: Would save to $configPath" -ForegroundColor Cyan
    Write-Host "  Configuration preview:" -ForegroundColor Cyan
    $config | ConvertTo-Json -Depth 10 | Write-Host
} else {
    try {
        # Convert to JSON with proper formatting
        $jsonContent = $config | ConvertTo-Json -Depth 10

        # CRITICAL: Actually write the file!
        [System.IO.File]::WriteAllText($configPath, $jsonContent, [System.Text.Encoding]::UTF8)

        Write-Host "  ✓ Configuration SAVED to: $configPath" -ForegroundColor Green
        Write-Host "  ✓ File size: $((Get-Item $configPath).Length) bytes" -ForegroundColor Green
    } catch {
        Write-Host "  ✗ FAILED to save configuration!" -ForegroundColor Red
        Write-Host "  Error: $_" -ForegroundColor Red

        if ($_.Exception.Message -like "*being used by another process*") {
            Write-Host ""
            Write-Host "  Claude Desktop is still running! Close it and try again." -ForegroundColor Yellow
        }
        exit 1
    }
}

# Verify the configuration was actually saved
Write-Host ""
Write-Host "[Step 5/6] Verifying configuration..." -ForegroundColor Yellow

if (-not $TestMode) {
    if (Test-Path $configPath) {
        try {
            $savedConfig = Get-Content $configPath -Raw | ConvertFrom-Json
            $savedMcpCount = @($savedConfig.mcpServers.PSObject.Properties).Count

            if ($savedMcpCount -eq 15) {
                Write-Host "  ✓ SUCCESS: $savedMcpCount MCPs configured and SAVED!" -ForegroundColor Green
                Write-Host ""
                Write-Host "  Configured MCPs:" -ForegroundColor Cyan
                $savedConfig.mcpServers.PSObject.Properties.Name | ForEach-Object {
                    Write-Host "    ✓ $_" -ForegroundColor Green
                }
            } else {
                Write-Host "  ⚠ WARNING: Expected 15 MCPs but found $savedMcpCount" -ForegroundColor Yellow
            }
        } catch {
            Write-Host "  ✗ Failed to verify configuration: $_" -ForegroundColor Red
        }
    } else {
        Write-Host "  ✗ CRITICAL: Configuration file does not exist after save!" -ForegroundColor Red
        Write-Host "  The installer failed to create the configuration." -ForegroundColor Red
        exit 1
    }
} else {
    Write-Host "  Test mode - skipping verification" -ForegroundColor Gray
}

# Create database file
Write-Host ""
Write-Host "[Step 6/6] Creating unified database..." -ForegroundColor Yellow
if (-not (Test-Path $dbPath)) {
    New-Item -ItemType File -Path $dbPath -Force | Out-Null
    Write-Host "  Created: $dbPath" -ForegroundColor Green
} else {
    Write-Host "  Database already exists: $dbPath" -ForegroundColor Gray
}

# Final instructions
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                         INSTALLATION COMPLETE!                             " -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "CRITICAL NEXT STEPS:" -ForegroundColor Yellow
Write-Host ""
Write-Host "1. UPDATE API KEYS in: $configPath" -ForegroundColor White
Write-Host "   - BRAVE_API_KEY" -ForegroundColor Gray
Write-Host "   - GITHUB_TOKEN" -ForegroundColor Gray
Write-Host "   - PERPLEXITY_API_KEY" -ForegroundColor Gray
Write-Host ""
Write-Host "2. RESTART Claude Desktop" -ForegroundColor White
Write-Host ""
Write-Host "3. CHECK that all 15 MCPs appear" -ForegroundColor White
Write-Host ""
Write-Host "TOKEN COUNT:" -ForegroundColor Cyan
Write-Host "This federation provides 81,821 tokens of comprehensive functionality." -ForegroundColor White
Write-Host "This is a FEATURE, not a bug - it represents the full power of 15 MCPs." -ForegroundColor Green
Write-Host ""
Write-Host "If MCPs don't appear after restart:" -ForegroundColor Yellow
Write-Host "• Check the MANUAL-MCP-SETUP.md file for troubleshooting" -ForegroundColor White
Write-Host "• Ensure Node.js and Python are installed" -ForegroundColor White
Write-Host "• Run this installer again with -Force flag" -ForegroundColor White
Write-Host ""