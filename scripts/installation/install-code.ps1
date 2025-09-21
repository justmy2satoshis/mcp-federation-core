# Claude Code CLI MCP Installation Script

param([switch]$Verbose = $false)

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$Username = $env:USERNAME

Write-Host "Installing MCPs for Claude Code CLI..." -ForegroundColor Cyan

# Array of MCP configurations
$mcps = @(
    @{
        Name = "expert-role-prompt"
        Command = "claude mcp add expert-role-prompt node `"$RepoRoot\mcps\expert-role-prompt\server.js`""
    },
    @{
        Name = "kimi-k2-resilient"
        Command = "claude mcp add kimi-k2-resilient python `"$RepoRoot\mcps\kimi-k2-resilient-enhanced\server.py`""
    },
    @{
        Name = "kimi-k2-code-context"
        Command = "claude mcp add kimi-k2-code-context python `"$RepoRoot\mcps\kimi-k2-code-context-enhanced\server.py`""
    },
    @{
        Name = "filesystem"
        Command = "claude mcp add filesystem npx -e NODE_NO_WARNINGS=1 -- -y `"@modelcontextprotocol/server-filesystem`" `"C:\Users\$Username\Documents`""
    },
    @{
        Name = "memory"
        Command = "claude mcp add memory npx -e NODE_NO_WARNINGS=1 -- -y `"@modelcontextprotocol/server-memory`""
    },
    @{
        Name = "sequential-thinking"
        Command = "claude mcp add sequential-thinking npx -e NODE_NO_WARNINGS=1 -- -y `"@modelcontextprotocol/server-sequential-thinking`""
    },
    @{
        Name = "desktop-commander"
        Command = "claude mcp add desktop-commander npx -e NODE_NO_WARNINGS=1 -- -y `"@wonderwhy-er/desktop-commander@latest`""
    },
    @{
        Name = "playwright"
        Command = "claude mcp add playwright npx -e NODE_NO_WARNINGS=1 -- -y `"@playwright/mcp@0.0.37`" --browser chromium"
    },
    @{
        Name = "sqlite"
        Command = "claude mcp add sqlite npx -e NODE_NO_WARNINGS=1 -- -y `"mcp-sqlite`" `"$RepoRoot\databases\sqlite\unified.db`""
    },
    @{
        Name = "git-ops"
        Command = "claude mcp add git-ops npx -e NODE_NO_WARNINGS=1 -e GIT_REPO_PATH=`"$RepoRoot`" -- -y `"@cyanheads/git-mcp-server`""
    }
)

# MCPs requiring API keys (will check .env file)
$apiMcps = @(
    @{
        Name = "perplexity"
        EnvVar = "PERPLEXITY_API_KEY"
        Command = "claude mcp add perplexity npx -e NODE_NO_WARNINGS=1 -e PERPLEXITY_API_KEY=`$KEY -- -y `"server-perplexity-ask`""
    },
    @{
        Name = "converse"
        EnvVars = @("OPENAI_API_KEY", "GEMINI_API_KEY")
        Command = "claude mcp add converse npx -e NODE_NO_WARNINGS=1 -e OPENAI_API_KEY=`$OPENAI -e GEMINI_API_KEY=`$GEMINI -- -y `"converse-mcp-server`""
    },
    @{
        Name = "github-manager"
        EnvVar = "GITHUB_PERSONAL_ACCESS_TOKEN"
        Command = "claude mcp add github-manager npx -e GITHUB_PERSONAL_ACCESS_TOKEN=`$KEY -- -y `"@modelcontextprotocol/server-github`""
    },
    @{
        Name = "web-search"
        EnvVar = "BRAVE_API_KEY"
        Command = "claude mcp add web-search npx -e NODE_NO_WARNINGS=1 -e BRAVE_API_KEY=`$KEY -- -y `"@modelcontextprotocol/server-brave-search`""
    },
    @{
        Name = "rag-context"
        Command = "claude mcp add rag-context npx -e NODE_NO_WARNINGS=1 -e RAG_DATA_DIR=`"$RepoRoot\ClaudeRAG\data`" -e RAG_LOG_DIR=`"$RepoRoot\ClaudeRAG\logs`" -- -y `"@notbnull/mcp-rag-context`""
    }
)

# Check if Claude CLI is available
if (-not (Get-Command claude -ErrorAction SilentlyContinue)) {
    Write-Host "❌ Claude CLI not found. Please install Claude Code first." -ForegroundColor Red
    exit 1
}

# Install MCPs
$installed = 0
$failed = 0

foreach ($mcp in $mcps) {
    Write-Host "  Installing $($mcp.Name)..." -ForegroundColor Gray
    try {
        Invoke-Expression $mcp.Command 2>$null
        $installed++
        if ($Verbose) {
            Write-Host "    ✓ Command: $($mcp.Command)" -ForegroundColor DarkGray
        }
    } catch {
        Write-Host "    ❌ Failed to install $($mcp.Name)" -ForegroundColor Red
        $failed++
    }
}

# Check for .env file for API key MCPs
$envFile = Join-Path $RepoRoot ".env"
if (Test-Path $envFile) {
    Write-Host "  Found .env file, configuring API-based MCPs..." -ForegroundColor Gray

    # Read .env file
    $envContent = Get-Content $envFile
    $envVars = @{}
    foreach ($line in $envContent) {
        if ($line -match '^([^=]+)=(.*)$') {
            $envVars[$matches[1]] = $matches[2]
        }
    }

    foreach ($mcp in $apiMcps) {
        if ($mcp.EnvVar -and $envVars[$mcp.EnvVar]) {
            $cmd = $mcp.Command -replace '\$KEY', $envVars[$mcp.EnvVar]
            if ($mcp.EnvVars) {
                $cmd = $cmd -replace '\$OPENAI', $envVars["OPENAI_API_KEY"]
                $cmd = $cmd -replace '\$GEMINI', $envVars["GEMINI_API_KEY"]
            }
            Write-Host "  Installing $($mcp.Name) with API key..." -ForegroundColor Gray
            try {
                Invoke-Expression $cmd 2>$null
                $installed++
            } catch {
                Write-Host "    ❌ Failed to install $($mcp.Name)" -ForegroundColor Red
                $failed++
            }
        } elseif ($mcp.Name -eq "rag-context") {
            Write-Host "  Installing $($mcp.Name)..." -ForegroundColor Gray
            try {
                Invoke-Expression $mcp.Command 2>$null
                $installed++
            } catch {
                Write-Host "    ❌ Failed to install $($mcp.Name)" -ForegroundColor Red
                $failed++
            }
        } else {
            Write-Host "  ⚠ Skipping $($mcp.Name) - API key not found in .env" -ForegroundColor Yellow
        }
    }
} else {
    Write-Host "  ⚠ No .env file found. Skipping API-based MCPs." -ForegroundColor Yellow
    Write-Host "    Create .env from .env.template and add your API keys" -ForegroundColor Gray
}

Write-Host ""
Write-Host "Installation Summary:" -ForegroundColor Cyan
Write-Host "  ✓ Installed: $installed MCPs" -ForegroundColor Green
if ($failed -gt 0) {
    Write-Host "  ❌ Failed: $failed MCPs" -ForegroundColor Red
}

# Verify installation
Write-Host ""
Write-Host "Verifying installation..." -ForegroundColor Yellow
$mcpList = claude mcp list 2>$null
if ($mcpList) {
    $connectedCount = ($mcpList | Select-String "Connected").Count
    Write-Host "  ✓ $connectedCount MCPs connected" -ForegroundColor Green
} else {
    Write-Host "  ⚠ Could not verify MCP connections" -ForegroundColor Yellow
}