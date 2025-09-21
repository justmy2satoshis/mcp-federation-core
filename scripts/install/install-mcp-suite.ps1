# MCP Federation Core Installer
# PowerShell script to install the complete MCP suite

param(
    [string]$InstallPath = "$env:USERPROFILE",
    [switch]$SkipDependencies = $false
)

Write-Host "================================================" -ForegroundColor Cyan
Write-Host "    MCP Federation Core Installer v2.0         " -ForegroundColor Cyan  
Write-Host "================================================" -ForegroundColor Cyan
Write-Host ""

# Function to check if a command exists
function Test-Command {
    param($Command)
    try {
        Get-Command $Command -ErrorAction Stop | Out-Null
        return $true
    } catch {
        return $false
    }
}

# Check prerequisites
Write-Host "[1/7] Checking prerequisites..." -ForegroundColor Yellow

if (-not $SkipDependencies) {
    # Check Node.js
    if (-not (Test-Command "node")) {
        Write-Host "  [!] Node.js not found. Please install from https://nodejs.org" -ForegroundColor Red
        exit 1
    } else {
        $nodeVersion = node --version
        Write-Host "  [+] Node.js found: $nodeVersion" -ForegroundColor Green
    }
    
    # Check Python
    if (-not (Test-Command "python")) {
        Write-Host "  [!] Python not found. Please install from https://python.org" -ForegroundColor Red
        exit 1
    } else {
        $pythonVersion = python --version
        Write-Host "  [+] Python found: $pythonVersion" -ForegroundColor Green
    }
    
    # Check Git
    if (-not (Test-Command "git")) {
        Write-Host "  [!] Git not found. Please install from https://git-scm.com" -ForegroundColor Red
        exit 1
    } else {
        $gitVersion = git --version
        Write-Host "  [+] Git found: $gitVersion" -ForegroundColor Green
    }
}

# Clone repository
Write-Host ""
Write-Host "[2/7] Cloning MCP Federation Core repository..." -ForegroundColor Yellow

$repoPath = Join-Path $InstallPath "mcp-federation-core"
if (Test-Path $repoPath) {
    Write-Host "  [!] Directory exists. Updating..." -ForegroundColor Yellow
    Push-Location $repoPath
    git pull origin main
    Pop-Location
} else {
    git clone https://github.com/justmy2satoshis/mcp-federation-core.git $repoPath
}

Write-Host "  [+] Repository ready" -ForegroundColor Green

# Copy unified database
Write-Host ""
Write-Host "[3/7] Setting up unified database..." -ForegroundColor Yellow

$dbSource = Join-Path $repoPath "mcp-unified.db"
$dbDest = Join-Path $InstallPath "mcp-unified.db"

if (Test-Path $dbDest) {
    Write-Host "  [?] Database exists. Backup? (y/n): " -ForegroundColor Yellow -NoNewline
    $backup = Read-Host
    if ($backup -eq "y") {
        $backupName = "mcp-unified.db.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
        Copy-Item $dbDest (Join-Path $InstallPath $backupName)
        Write-Host "  [+] Backup created: $backupName" -ForegroundColor Green
    }
}

Copy-Item $dbSource $dbDest -Force
Write-Host "  [+] Database installed" -ForegroundColor Green

# Copy MCP servers
Write-Host ""
Write-Host "[4/7] Installing MCP servers..." -ForegroundColor Yellow

$serversSource = Join-Path $repoPath "mcp-servers"
$serversDest = Join-Path $InstallPath "mcp-servers"

if (-not (Test-Path $serversDest)) {
    New-Item -ItemType Directory -Path $serversDest | Out-Null
}

# Copy enhanced MCPs
$mcps = @(
    "expert-role-prompt",
    "kimi-k2-code-context-enhanced",
    "kimi-k2-resilient-enhanced"
)

foreach ($mcp in $mcps) {
    $source = Join-Path $serversSource $mcp
    $dest = Join-Path $serversDest $mcp
    
    if (Test-Path $source) {
        Copy-Item -Path $source -Destination $dest -Recurse -Force
        Write-Host "  [+] Installed: $mcp" -ForegroundColor Green
    } else {
        Write-Host "  [!] Warning: $mcp not found in repository" -ForegroundColor Yellow
    }
}

# Install npm dependencies for expert-role-prompt
Write-Host ""
Write-Host "[5/7] Installing npm dependencies..." -ForegroundColor Yellow

$expertPath = Join-Path $serversDest "expert-role-prompt"
if (Test-Path $expertPath) {
    Push-Location $expertPath
    npm install
    Pop-Location
    Write-Host "  [+] npm dependencies installed" -ForegroundColor Green
}

# Install Python dependencies
Write-Host ""
Write-Host "[6/7] Installing Python dependencies..." -ForegroundColor Yellow

$pythonDeps = @("sqlite3", "json", "typing", "asyncio", "datetime")
pip install psutil | Out-Null
Write-Host "  [+] Python dependencies ready" -ForegroundColor Green

# Configure Claude Desktop
Write-Host ""
Write-Host "[7/7] Configuring Claude Desktop..." -ForegroundColor Yellow

$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$configDir = Split-Path $configPath -Parent

if (-not (Test-Path $configDir)) {
    New-Item -ItemType Directory -Path $configDir | Out-Null
}

# Create config object
$config = @{
    mcpServers = @{
        "expert-role-prompt" = @{
            command = "node"
            args = @("$serversDest\expert-role-prompt\server.js")
        }
        "kimi-k2-code-context-enhanced" = @{
            command = "python"
            args = @("$serversDest\kimi-k2-code-context-enhanced\server.py")
        }
        "kimi-k2-resilient-enhanced" = @{
            command = "python"
            args = @("$serversDest\kimi-k2-resilient-enhanced\server.py")
        }
    }
}

# Backup existing config
if (Test-Path $configPath) {
    $backupConfig = "$configPath.backup_$(Get-Date -Format 'yyyyMMdd_HHmmss')"
    Copy-Item $configPath $backupConfig
    Write-Host "  [+] Config backed up" -ForegroundColor Green
    
    # Merge with existing config
    $existingConfig = Get-Content $configPath | ConvertFrom-Json
    if ($existingConfig.mcpServers) {
        foreach ($server in $config.mcpServers.Keys) {
            $existingConfig.mcpServers | Add-Member -Name $server -Value $config.mcpServers.$server -MemberType NoteProperty -Force
        }
        $config = $existingConfig
    }
}

# Write config
$config | ConvertTo-Json -Depth 10 | Set-Content $configPath
Write-Host "  [+] Claude Desktop configured" -ForegroundColor Green

# Copy test scripts
Write-Host ""
Write-Host "Copying test scripts..." -ForegroundColor Yellow
Copy-Item (Join-Path $repoPath "test_*.py") $InstallPath -Force
Copy-Item (Join-Path $repoPath "check_*.py") $InstallPath -Force
Copy-Item (Join-Path $repoPath "benchmark_*.py") $InstallPath -Force
Write-Host "  [+] Test scripts installed" -ForegroundColor Green

# Final instructions
Write-Host ""
Write-Host "================================================" -ForegroundColor Green
Write-Host "    Installation Complete!" -ForegroundColor Green
Write-Host "================================================" -ForegroundColor Green
Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "1. Restart Claude Desktop"
Write-Host "2. Test with: python $InstallPath\test_mcp_persistence.py"
Write-Host "3. Benchmark with: python $InstallPath\benchmark_mcp_performance.py"
Write-Host ""
Write-Host "MCP Servers installed at: $serversDest" -ForegroundColor Gray
Write-Host "Database installed at: $dbDest" -ForegroundColor Gray
Write-Host ""
Write-Host "Repository: https://github.com/justmy2satoshis/mcp-federation-core" -ForegroundColor Blue
