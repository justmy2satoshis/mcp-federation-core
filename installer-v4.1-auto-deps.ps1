# MCP Federation Core Complete Installer v4.1 - ZERO-DEPENDENCY VERSION
# This version automatically installs Python, Node.js, and Git if missing
# GitHub: https://github.com/justmy2satoshis/mcp-federation-core

param(
    [switch]$SkipDependencies,
    [switch]$SkipOllama,
    [switch]$SkipPython,
    [switch]$QuickInstall,
    [switch]$UpdateOnly,
    [switch]$Force,
    [switch]$WhatIf
)

$ErrorActionPreference = "Stop"
$ProgressPreference = "SilentlyContinue"

# Display banner
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "              MCP FEDERATION CORE v4.1 - ZERO DEPENDENCY EDITION           " -ForegroundColor Cyan
Write-Host "            Automatic Installation of Python, Node.js, Git & 15 MCPs       " -ForegroundColor White
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Check if running as administrator
function Test-AdminRights {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
}

# Function to install dependencies automatically
function Install-Dependencies {
    if ($SkipDependencies) {
        Write-Host "[DEPENDENCIES] Skipping dependency installation (-SkipDependencies flag)" -ForegroundColor Yellow
        return
    }

    Write-Host "[DEPENDENCIES] Checking and installing required software..." -ForegroundColor Cyan
    Write-Host ""

    $needsRestart = $false

    # Check and install Python
    Write-Host "  Python:" -ForegroundColor White
    $pythonCmd = Get-Command python -ErrorAction SilentlyContinue
    if (-not $pythonCmd) {
        $pythonCmd = Get-Command python3 -ErrorAction SilentlyContinue
    }

    if (-not $pythonCmd) {
        Write-Host "    Not found. Installing Python 3.12..." -ForegroundColor Yellow

        if (-not (Test-AdminRights)) {
            Write-Host "    ⚠ Administrator rights required for Python installation" -ForegroundColor Red
            Write-Host "    Please run this script as Administrator" -ForegroundColor Yellow
            exit 1
        }

        try {
            $pythonUrl = "https://www.python.org/ftp/python/3.12.0/python-3.12.0-amd64.exe"
            $pythonInstaller = "$env:TEMP\python-installer.exe"

            Write-Host "    Downloading Python installer..." -ForegroundColor Gray
            Invoke-WebRequest -Uri $pythonUrl -OutFile $pythonInstaller -UseBasicParsing

            Write-Host "    Installing Python (this may take a few minutes)..." -ForegroundColor Gray
            Start-Process -FilePath $pythonInstaller -ArgumentList "/quiet", "InstallAllUsers=1", "PrependPath=1", "Include_pip=1", "Include_launcher=1" -Wait -NoNewWindow

            Remove-Item $pythonInstaller -Force -ErrorAction SilentlyContinue
            Write-Host "    ✅ Python installed successfully" -ForegroundColor Green
            $needsRestart = $true
        }
        catch {
            Write-Host "    ❌ Failed to install Python: $_" -ForegroundColor Red
            Write-Host "    Please install Python manually from: https://www.python.org" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    ✅ Found: $($pythonCmd.Version)" -ForegroundColor Green
    }

    # Check and install Node.js
    Write-Host "  Node.js:" -ForegroundColor White
    $nodeCmd = Get-Command node -ErrorAction SilentlyContinue

    if (-not $nodeCmd) {
        Write-Host "    Not found. Installing Node.js v20 LTS..." -ForegroundColor Yellow

        if (-not (Test-AdminRights)) {
            Write-Host "    ⚠ Administrator rights required for Node.js installation" -ForegroundColor Red
            Write-Host "    Please run this script as Administrator" -ForegroundColor Yellow
            exit 1
        }

        try {
            $nodeUrl = "https://nodejs.org/dist/v20.11.0/node-v20.11.0-x64.msi"
            $nodeInstaller = "$env:TEMP\node-installer.msi"

            Write-Host "    Downloading Node.js installer..." -ForegroundColor Gray
            Invoke-WebRequest -Uri $nodeUrl -OutFile $nodeInstaller -UseBasicParsing

            Write-Host "    Installing Node.js (this may take a few minutes)..." -ForegroundColor Gray
            Start-Process msiexec.exe -ArgumentList "/i", $nodeInstaller, "/quiet", "/norestart", "ADDLOCAL=ALL" -Wait -NoNewWindow

            Remove-Item $nodeInstaller -Force -ErrorAction SilentlyContinue
            Write-Host "    ✅ Node.js installed successfully" -ForegroundColor Green
            $needsRestart = $true
        }
        catch {
            Write-Host "    ❌ Failed to install Node.js: $_" -ForegroundColor Red
            Write-Host "    Please install Node.js manually from: https://nodejs.org" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    ✅ Found: node $(node --version 2>$null)" -ForegroundColor Green
    }

    # Check and install Git
    Write-Host "  Git:" -ForegroundColor White
    $gitCmd = Get-Command git -ErrorAction SilentlyContinue

    if (-not $gitCmd) {
        Write-Host "    Not found. Installing Git..." -ForegroundColor Yellow

        if (-not (Test-AdminRights)) {
            Write-Host "    ⚠ Administrator rights required for Git installation" -ForegroundColor Red
            Write-Host "    Please run this script as Administrator" -ForegroundColor Yellow
            exit 1
        }

        try {
            $gitUrl = "https://github.com/git-for-windows/git/releases/download/v2.43.0.windows.1/Git-2.43.0-64-bit.exe"
            $gitInstaller = "$env:TEMP\git-installer.exe"

            Write-Host "    Downloading Git installer..." -ForegroundColor Gray
            Invoke-WebRequest -Uri $gitUrl -OutFile $gitInstaller -UseBasicParsing

            Write-Host "    Installing Git (this may take a few minutes)..." -ForegroundColor Gray
            Start-Process -FilePath $gitInstaller -ArgumentList "/VERYSILENT", "/NORESTART", "/NOCANCEL", "/SP-", "/CLOSEAPPLICATIONS", "/RESTARTAPPLICATIONS", "/COMPONENTS=icons,ext\reg\shellhere,assoc,assoc_sh" -Wait -NoNewWindow

            Remove-Item $gitInstaller -Force -ErrorAction SilentlyContinue
            Write-Host "    ✅ Git installed successfully" -ForegroundColor Green
            $needsRestart = $true
        }
        catch {
            Write-Host "    ❌ Failed to install Git: $_" -ForegroundColor Red
            Write-Host "    Please install Git manually from: https://git-scm.com" -ForegroundColor Yellow
        }
    } else {
        Write-Host "    ✅ Found: git $(git --version 2>$null)" -ForegroundColor Green
    }

    # Refresh PATH if we installed anything
    if ($needsRestart) {
        Write-Host ""
        Write-Host "  Refreshing system PATH..." -ForegroundColor Yellow
        $env:Path = [System.Environment]::GetEnvironmentVariable("Path","Machine") + ";" + [System.Environment]::GetEnvironmentVariable("Path","User")

        Write-Host "  ⚠ New software installed. You may need to restart your terminal." -ForegroundColor Yellow
        Write-Host "  If commands are not found, please close and reopen PowerShell." -ForegroundColor Yellow
        Write-Host ""

        # Wait a moment for PATH to update
        Start-Sleep -Seconds 3
    }

    Write-Host ""
}

# Configuration
$baseDir = "$env:USERPROFILE\mcp-servers"
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = "$baseDir\backups\$timestamp"
$dbPath = "$baseDir\mcp-unified.db"

# MCP Repository URLs
$mcpRepositories = @{
    'converse' = @{
        url = "https://github.com/justmy2satoshis/converse-mcp.git"
        type = "node"
        entry = "index.js"
    }
    'expert-role-prompt' = @{
        url = "https://github.com/justmy2satoshis/expert-role-mcp.git"
        type = "node"
        entry = "index.js"
    }
    'desktop-commander' = @{
        url = "https://github.com/DesktopCommanderHQ/desktop-commander.git"
        type = "node"
        entry = "dist/index.js"
        needsBuild = $true
    }
    'sequential-thinking' = @{
        url = "https://github.com/justmy2satoshis/sequential-thinking-mcp.git"
        type = "node"
        entry = "index.js"
    }
    'perplexity' = @{
        url = "https://github.com/justmy2satoshis/perplexity-mcp.git"
        type = "node"
        entry = "index.js"
    }
}

# NPX-based MCPs (from npm registry)
$npxMCPs = @{
    'sqlite' = '@modelcontextprotocol/server-sqlite'
    'filesystem' = '@modelcontextprotocol/server-filesystem'
    'memory' = '@modelcontextprotocol/server-memory'
    'github-manager' = '@modelcontextprotocol/server-github'
    'web-search' = '@modelcontextprotocol/server-brave-search'
    'playwright' = '@modelcontextprotocol/server-playwright'
    'git-ops' = '@modelcontextprotocol/server-git'
}

# Python-based MCPs
$pythonMCPs = @{
    'kimi-k2-resilient-enhanced' = @{
        module = "kimi_k2_resilient"
        package = "kimi-k2-mcp"
    }
    'kimi-k2-code-context-enhanced' = @{
        module = "kimi_k2_code_context"
        package = "kimi-k2-code-context"
    }
    'rag-context' = @{
        module = "rag_context"
        package = "rag-context-mcp"
    }
}

# Function to create backup
function New-ConfigBackup {
    param(
        [string]$ConfigPath,
        [string]$BackupDir
    )

    if (Test-Path $ConfigPath) {
        New-Item -ItemType Directory -Force -Path $BackupDir | Out-Null
        $backupPath = Join-Path $BackupDir "claude_desktop_config.json"
        Copy-Item $ConfigPath $backupPath -Force
        return $backupPath
    }
    return $null
}

# Function to clone or update repository
function Update-Repository {
    param(
        [string]$RepoUrl,
        [string]$TargetPath,
        [string]$Name
    )

    Write-Host "  Setting up $Name..." -ForegroundColor Gray

    # Check if git is available
    if (-not (Get-Command git -ErrorAction SilentlyContinue)) {
        Write-Host "    ⚠ Git not available, skipping repository clone" -ForegroundColor Yellow
        return $false
    }

    if (Test-Path "$TargetPath\.git") {
        # Repository exists, pull latest
        Push-Location $TargetPath
        try {
            git pull --quiet 2>$null
            Write-Host "    Updated from repository" -ForegroundColor Green
        }
        catch {
            Write-Host "    Warning: Could not update (using existing)" -ForegroundColor Yellow
        }
        finally {
            Pop-Location
        }
    }
    else {
        # Clone new repository
        try {
            # Remove directory if it exists but isn't a git repo
            if (Test-Path $TargetPath) {
                Remove-Item -Recurse -Force $TargetPath
            }

            git clone $RepoUrl $TargetPath --quiet 2>$null
            Write-Host "    Cloned from repository" -ForegroundColor Green
        }
        catch {
            Write-Host "    Error: Could not clone repository" -ForegroundColor Red
            return $false
        }
    }

    return $true
}

# Function to install Node dependencies
function Install-NodeDependencies {
    param(
        [string]$Path,
        [string]$Name
    )

    if (Test-Path "$Path\package.json") {
        Push-Location $Path
        try {
            Write-Host "    Installing dependencies..." -ForegroundColor Gray -NoNewline
            npm install --quiet 2>$null
            Write-Host " Done" -ForegroundColor Green
        }
        catch {
            Write-Host " Failed" -ForegroundColor Yellow
        }
        finally {
            Pop-Location
        }
    }
}

# Main installation logic
if ($WhatIf) {
    Write-Host "[WHATIF MODE] No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Install dependencies first
if (-not $WhatIf -and -not $UpdateOnly) {
    Install-Dependencies
}

# Re-check prerequisites after installation
Write-Host "[PREREQUISITES] Verifying system requirements..." -ForegroundColor Yellow

$prereqMet = $true
$prereqs = @(
    @{Name="Python"; Command="python"; Version="--version"},
    @{Name="Node.js"; Command="node"; Version="--version"},
    @{Name="Git"; Command="git"; Version="--version"},
    @{Name="npm"; Command="npm"; Version="--version"}
)

foreach ($prereq in $prereqs) {
    try {
        $output = & $prereq.Command $prereq.Version 2>&1
        Write-Host "  ✓ $($prereq.Name) - $output" -ForegroundColor Green
    }
    catch {
        Write-Host "  ✗ $($prereq.Name) - Not found" -ForegroundColor Red
        $prereqMet = $false
    }
}

if (-not $prereqMet -and -not $Force) {
    Write-Host ""
    Write-Host "Some prerequisites are still missing after installation attempt." -ForegroundColor Red
    Write-Host "Please restart your terminal and run this script again." -ForegroundColor Yellow
    Write-Host "Or use -Force to continue anyway." -ForegroundColor Yellow
    exit 1
}

# Create required directories
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[SETUP] Creating directory structure..." -ForegroundColor Yellow

    @($baseDir, "$env:APPDATA\Claude") | ForEach-Object {
        if (-not (Test-Path $_)) {
            New-Item -ItemType Directory -Force -Path $_ | Out-Null
            Write-Host "  Created: $_" -ForegroundColor Green
        }
    }
}

# Backup existing config
if ((Test-Path $configPath) -and -not $WhatIf) {
    Write-Host ""
    Write-Host "[BACKUP] Creating configuration backup..." -ForegroundColor Yellow
    $backupPath = New-ConfigBackup -ConfigPath $configPath -BackupDir $backupDir
    if ($backupPath) {
        Write-Host "  Saved: $backupPath" -ForegroundColor Green
    }
}

# Download and setup Node.js MCPs
if (-not $WhatIf -and -not $UpdateOnly) {
    Write-Host ""
    Write-Host "[NODE.JS MCPs] Installing Node-based MCPs..." -ForegroundColor Yellow

    foreach ($mcpName in $mcpRepositories.Keys) {
        $mcp = $mcpRepositories[$mcpName]
        $targetPath = Join-Path $baseDir $mcpName

        if (Update-Repository -RepoUrl $mcp.url -TargetPath $targetPath -Name $mcpName) {
            Install-NodeDependencies -Path $targetPath -Name $mcpName

            if ($mcp.needsBuild) {
                Push-Location $targetPath
                try {
                    Write-Host "    Building..." -ForegroundColor Gray -NoNewline
                    npm run build --quiet 2>$null
                    Write-Host " Done" -ForegroundColor Green
                }
                catch {
                    Write-Host " Failed" -ForegroundColor Yellow
                }
                finally {
                    Pop-Location
                }
            }
        }
    }
}

# Install Python packages
if (-not $SkipPython -and -not $UpdateOnly -and -not $WhatIf) {
    Write-Host ""
    Write-Host "[PYTHON MCPs] Installing Python-based MCPs..." -ForegroundColor Yellow

    # First ensure pip is up to date
    Write-Host "  Updating pip..." -ForegroundColor Gray
    python -m pip install --upgrade pip --quiet 2>$null

    foreach ($mcpName in $pythonMCPs.Keys) {
        $package = $pythonMCPs[$mcpName].package
        Write-Host "  Installing $mcpName..." -ForegroundColor Gray -NoNewline

        try {
            python -m pip install -q $package 2>$null
            Write-Host " Done" -ForegroundColor Green
        }
        catch {
            Write-Host " Failed (package may not exist yet)" -ForegroundColor Yellow
        }
    }
}

# Configure all MCPs
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[CONFIGURATION] Configuring MCPs in Claude Desktop..." -ForegroundColor Yellow

    # Load or create config
    if (Test-Path $configPath) {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
    } else {
        $config = @{ mcpServers = @{} } | ConvertTo-Json | ConvertFrom-Json
    }

    # Ensure mcpServers property exists
    if (-not $config.mcpServers) {
        $config | Add-Member -NotePropertyName "mcpServers" -NotePropertyValue @{} -Force
    }

    # Configure Node.js MCPs from repositories
    foreach ($mcpName in $mcpRepositories.Keys) {
        $mcp = $mcpRepositories[$mcpName]
        $entryPath = Join-Path $baseDir $mcpName | Join-Path -ChildPath $mcp.entry

        $mcpEntry = @{
            command = "node"
            args = @($entryPath)
        }

        # Add environment variables if needed
        if ($mcpName -eq 'perplexity') {
            $mcpEntry.env = @{ PERPLEXITY_API_KEY = "YOUR_PERPLEXITY_API_KEY" }
        }

        if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
            $config.mcpServers.PSObject.Properties.Remove($mcpName)
        }
        $config.mcpServers | Add-Member -NotePropertyName $mcpName -NotePropertyValue $mcpEntry -Force
        Write-Host "  Configured: $mcpName" -ForegroundColor Gray
    }

    # Configure NPX-based MCPs
    foreach ($mcpName in $npxMCPs.Keys) {
        $packageName = $npxMCPs[$mcpName]

        $mcpEntry = @{
            command = "npx"
            args = @("-y", $packageName)
        }

        # Add specific configurations
        switch ($mcpName) {
            'sqlite' {
                $mcpEntry.args += $dbPath
            }
            'filesystem' {
                $mcpEntry.env = @{ ALLOWED_PATHS = $env:USERPROFILE }
            }
            'github-manager' {
                $mcpEntry.env = @{ GITHUB_TOKEN = "YOUR_GITHUB_TOKEN" }
            }
            'web-search' {
                $mcpEntry.env = @{ BRAVE_API_KEY = "YOUR_BRAVE_API_KEY" }
            }
        }

        if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
            $config.mcpServers.PSObject.Properties.Remove($mcpName)
        }
        $config.mcpServers | Add-Member -NotePropertyName $mcpName -NotePropertyValue $mcpEntry -Force
        Write-Host "  Configured: $mcpName" -ForegroundColor Gray
    }

    # Configure Python MCPs
    foreach ($mcpName in $pythonMCPs.Keys) {
        $module = $pythonMCPs[$mcpName].module

        $mcpEntry = @{
            command = "python"
            args = @("-m", $module)
        }

        # Add environment variables if needed
        switch ($mcpName) {
            'kimi-k2-resilient-enhanced' {
                $mcpEntry.env = @{ KIMI_DB_PATH = "$baseDir\kimi-resilient.db" }
            }
            'rag-context' {
                $mcpEntry.env = @{ RAG_DB_PATH = "$baseDir\rag-context.db" }
            }
        }

        if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
            $config.mcpServers.PSObject.Properties.Remove($mcpName)
        }
        $config.mcpServers | Add-Member -NotePropertyName $mcpName -NotePropertyValue $mcpEntry -Force
        Write-Host "  Configured: $mcpName" -ForegroundColor Gray
    }

    # Save configuration
    Write-Host ""
    Write-Host "  Saving configuration..." -ForegroundColor Yellow

    try {
        $jsonContent = $config | ConvertTo-Json -Depth 10
        $jsonContent | Set-Content -Path $configPath -Encoding UTF8 -Force
        Write-Host "  Configuration saved successfully!" -ForegroundColor Green

        # Verify
        $verification = Get-Content $configPath -Raw | ConvertFrom-Json
        $verifiedCount = @($verification.mcpServers.PSObject.Properties.Name).Count
        Write-Host "  Verified: $verifiedCount MCPs configured" -ForegroundColor Green
    }
    catch {
        Write-Host "  ERROR: Failed to save configuration: $_" -ForegroundColor Red
        exit 1
    }
}

# Create database
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[DATABASE] Setting up unified database..." -ForegroundColor Yellow

    if (-not (Test-Path $dbPath)) {
        New-Item -ItemType File -Path $dbPath -Force | Out-Null
        Write-Host "  Created: $dbPath" -ForegroundColor Green
    }
    else {
        Write-Host "  Exists: $dbPath" -ForegroundColor Gray
    }
}

# Summary
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Green
Write-Host "                    🎉 INSTALLATION COMPLETE 🎉                            " -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

if (-not $WhatIf) {
    $finalConfig = Get-Content $configPath -Raw | ConvertFrom-Json
    $actualMCPCount = @($finalConfig.mcpServers.PSObject.Properties.Name).Count

    Write-Host "Summary:" -ForegroundColor Cyan
    Write-Host "  MCPs Configured: $actualMCPCount" -ForegroundColor White
    Write-Host "  Database: $dbPath" -ForegroundColor White

    if ($backupPath) {
        Write-Host "  Backup: $backupPath" -ForegroundColor White
    }
}

Write-Host ""
Write-Host "Next Steps:" -ForegroundColor Cyan
Write-Host "  1. Configure API keys (optional):" -ForegroundColor White
Write-Host "     - GITHUB_TOKEN for github-manager" -ForegroundColor Gray
Write-Host "     - BRAVE_API_KEY for web-search" -ForegroundColor Gray
Write-Host "     - PERPLEXITY_API_KEY for perplexity" -ForegroundColor Gray
Write-Host ""
Write-Host "  2. Restart Claude Desktop" -ForegroundColor White
Write-Host ""
Write-Host "  3. Verify MCPs appear in Claude Desktop settings" -ForegroundColor White
Write-Host ""

if ($WhatIf) {
    Write-Host "[WHATIF] No changes were made. Remove -WhatIf to perform installation." -ForegroundColor Yellow
} else {
    Write-Host "🚀 Claude Desktop is now supercharged with 15 MCPs!" -ForegroundColor Cyan
    Write-Host ""
}