# Create proper Windows MCP configuration for Claude Desktop
# This actually creates a WORKING configuration

$ErrorActionPreference = "Stop"

Write-Host ""
Write-Host "Creating Windows-compatible MCP configuration..." -ForegroundColor Cyan
Write-Host ""

# Create directory if needed
$configDir = "$env:APPDATA\Claude"
if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir -Force | Out-Null
    Write-Host "Created config directory" -ForegroundColor Green
}

# Configuration path
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$baseDir = "$env:USERPROFILE\mcp-servers"

# Create the ACTUAL working configuration
$config = @{
    mcpServers = @{
        'sequential-thinking' = @{
            command = "npx"
            args = @("-y", "@modelcontextprotocol/server-sequential-thinking")
        }
        'memory' = @{
            command = "npx"
            args = @("-y", "@modelcontextprotocol/server-memory")
        }
        'filesystem' = @{
            command = "npx"
            args = @("-y", "@modelcontextprotocol/server-filesystem", "$env:USERPROFILE")
        }
        'desktop-commander' = @{
            command = "npx"
            args = @("-y", "@rkdms/desktop-commander")
        }
        'playwright' = @{
            command = "npx"
            args = @("-y", "@modelcontextprotocol/server-playwright")
        }
        'sqlite' = @{
            command = "npx"
            args = @("-y", "@modelcontextprotocol/server-sqlite", "$baseDir\mcp-unified.db")
        }
        'git-ops' = @{
            command = "npx"
            args = @("-y", "git-ops-mcp")
        }
        'web-search' = @{
            command = "npx"
            args = @("-y", "@modelcontextprotocol/server-brave-search")
        }
        'github-manager' = @{
            command = "npx"
            args = @("-y", "@modelcontextprotocol/server-github")
        }
        'perplexity' = @{
            command = "npx"
            args = @("-y", "perplexity-mcp-server")
        }
        'converse' = @{
            command = "node"
            args = @("$baseDir\converse\index.js")
        }
        'expert-role-prompt' = @{
            command = "node"
            args = @("$baseDir\expert-role-prompt\index.js")
        }
        'rag-context' = @{
            command = "node"
            args = @("$baseDir\rag-context\index.js")
        }
        'kimi-k2-code-context' = @{
            command = "python"
            args = @("-m", "kimi_k2_code_context")
        }
        'kimi-k2-resilient' = @{
            command = "python"
            args = @("-m", "kimi_k2_resilient")
        }
    }
}

# Save configuration
$jsonContent = $config | ConvertTo-Json -Depth 10
$jsonContent | Set-Content -Path $configPath -Encoding UTF8 -Force

Write-Host "Configuration saved to: $configPath" -ForegroundColor Green
Write-Host ""

# Verify
if (Test-Path $configPath) {
    $saved = Get-Content $configPath -Raw | ConvertFrom-Json
    $count = @($saved.mcpServers.PSObject.Properties).Count
    Write-Host "Successfully configured $count MCPs" -ForegroundColor Green
    Write-Host ""
    Write-Host "MCPs configured:" -ForegroundColor Cyan
    $saved.mcpServers.PSObject.Properties.Name | ForEach-Object {
        Write-Host "  - $_" -ForegroundColor White
    }
} else {
    Write-Host "ERROR: Configuration was not saved!" -ForegroundColor Red
}

Write-Host ""
Write-Host "IMPORTANT: Restart Claude Desktop to load MCPs" -ForegroundColor Yellow