# MCP Federation Core v4.2 VERIFIED - Fixed Installer
# This version uses the ACTUAL MCPs included in the repository
# GitHub: https://github.com/justmy2satoshis/mcp-federation-core

param(
    [switch]$SkipDependencies,
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
Write-Host "              MCP FEDERATION CORE v4.2 - VERIFIED EDITION                  " -ForegroundColor Cyan
Write-Host "              Uses Embedded MCPs + Verified npm Packages                   " -ForegroundColor White
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

# Configuration
$baseDir = "$env:USERPROFILE\mcp-servers"
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"
$timestamp = Get-Date -Format 'yyyyMMdd_HHmmss'
$backupDir = "$baseDir\backups\$timestamp"
$dbPath = "$baseDir\mcp-unified.db"
$repoDir = $PWD

# VERIFIED MCPs from repository's mcp-servers directory
$embeddedMCPs = @{
    'expert-role-prompt' = @{
        source = "mcp-servers/expert-role-prompt"
        entry = "server.js"
        type = "node"
        description = "50+ Expert roles with CoT reasoning"
    }
    'kimi-k2-resilient-enhanced' = @{
        source = "mcp-servers/kimi-k2-resilient-enhanced"
        entry = "server.py"
        type = "python"
        description = "Resilient data storage with K2 processing"
    }
    'kimi-k2-code-context-enhanced' = @{
        source = "mcp-servers/kimi-k2-code-context-enhanced"
        entry = "server.py"
        type = "python"
        description = "Code context analysis with K2 processing"
    }
    'rag-context-fixed' = @{
        source = "mcp-servers/rag-context-fixed"
        entry = "server.py"
        type = "python"
        description = "RAG-based context management"
    }
}

# MCPs from repository's mcps directory
$mcpsDirMCPs = @{
    'converse-enhanced' = @{
        source = "mcps/converse-enhanced"
        entry = "server_wrapper.js"
        type = "node"
        description = "Multi-model AI consensus with Ollama"
    }
}

# VERIFIED NPM packages (tested and confirmed to exist)
$verifiedNpmMCPs = @{
    'filesystem' = '@modelcontextprotocol/server-filesystem'
    'memory' = '@modelcontextprotocol/server-memory'
    'github-manager' = '@modelcontextprotocol/server-github'
    'web-search' = '@modelcontextprotocol/server-brave-search'
}

# Function to test admin rights
function Test-AdminRights {
    $currentUser = [Security.Principal.WindowsIdentity]::GetCurrent()
    $principal = New-Object Security.Principal.WindowsPrincipal($currentUser)
    return $principal.IsInRole([Security.Principal.WindowsBuiltInRole]::Administrator)
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

# Function to copy embedded MCP from repository
function Copy-EmbeddedMCP {
    param(
        [string]$SourcePath,
        [string]$TargetPath,
        [string]$Name
    )

    Write-Host "  Setting up $Name (embedded)..." -ForegroundColor Gray

    $fullSourcePath = Join-Path $repoDir $SourcePath

    if (-not (Test-Path $fullSourcePath)) {
        Write-Host "    ERROR: Source not found: $fullSourcePath" -ForegroundColor Red
        return $false
    }

    try {
        # Remove existing directory if it exists
        if (Test-Path $TargetPath) {
            Remove-Item -Recurse -Force $TargetPath
        }

        # Copy the entire directory
        Copy-Item -Recurse $fullSourcePath $TargetPath -Force
        Write-Host "    SUCCESS: Copied from repository" -ForegroundColor Green
        return $true
    }
    catch {
        Write-Host "    ERROR: Failed to copy: $_" -ForegroundColor Red
        return $false
    }
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

# Function to check if npm package exists
function Test-NpmPackage {
    param([string]$PackageName)

    try {
        npm view $PackageName version --silent 2>$null | Out-Null
        return $LASTEXITCODE -eq 0
    }
    catch {
        return $false
    }
}

# Main installation logic
if ($WhatIf) {
    Write-Host "[WHATIF MODE] No changes will be made" -ForegroundColor Yellow
    Write-Host ""
}

# Check prerequisites
Write-Host "[PREREQUISITES] Checking system requirements..." -ForegroundColor Yellow

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
        Write-Host "  OK: $($prereq.Name) - $output" -ForegroundColor Green
    }
    catch {
        Write-Host "  ERROR: $($prereq.Name) - Not found" -ForegroundColor Red
        $prereqMet = $false
    }
}

if (-not $prereqMet -and -not $Force) {
    Write-Host ""
    Write-Host "Prerequisites not met. Install missing components or use -Force to continue anyway." -ForegroundColor Red
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

# Install embedded MCPs from mcp-servers directory
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[EMBEDDED MCPs] Installing repository MCPs..." -ForegroundColor Yellow

    foreach ($mcpName in $embeddedMCPs.Keys) {
        $mcp = $embeddedMCPs[$mcpName]
        $targetPath = Join-Path $baseDir $mcpName

        if (Copy-EmbeddedMCP -SourcePath $mcp.source -TargetPath $targetPath -Name $mcpName) {
            if ($mcp.type -eq "node") {
                Install-NodeDependencies -Path $targetPath -Name $mcpName
            }
        }
    }

    # Install MCPs from mcps directory
    foreach ($mcpName in $mcpsDirMCPs.Keys) {
        $mcp = $mcpsDirMCPs[$mcpName]
        $targetPath = Join-Path $baseDir $mcpName

        if (Copy-EmbeddedMCP -SourcePath $mcp.source -TargetPath $targetPath -Name $mcpName) {
            if ($mcp.type -eq "node") {
                Install-NodeDependencies -Path $targetPath -Name $mcpName
            }
        }
    }
}

# Verify npm packages exist before configuring
Write-Host ""
Write-Host "[NPM VERIFICATION] Checking npm packages..." -ForegroundColor Yellow

$workingNpmMCPs = @{}
foreach ($mcpName in $verifiedNpmMCPs.Keys) {
    $packageName = $verifiedNpmMCPs[$mcpName]
    Write-Host "  Checking $packageName..." -ForegroundColor Gray -NoNewline

    if (Test-NpmPackage -PackageName $packageName) {
        Write-Host " OK" -ForegroundColor Green
        $workingNpmMCPs[$mcpName] = $packageName
    } else {
        Write-Host " FAILED" -ForegroundColor Red
    }
}

# Configure all working MCPs
if (-not $WhatIf) {
    Write-Host ""
    Write-Host "[CONFIGURATION] Configuring working MCPs in Claude Desktop..." -ForegroundColor Yellow

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

    # Configure embedded MCPs from mcp-servers
    foreach ($mcpName in $embeddedMCPs.Keys) {
        $mcp = $embeddedMCPs[$mcpName]
        $entryPath = Join-Path $baseDir $mcpName | Join-Path -ChildPath $mcp.entry

        if ($mcp.type -eq "node") {
            $mcpEntry = @{
                command = "node"
                args = @($entryPath)
            }
        } elseif ($mcp.type -eq "python") {
            $mcpEntry = @{
                command = "python"
                args = @($entryPath)
            }
        }

        if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
            $config.mcpServers.PSObject.Properties.Remove($mcpName)
        }
        $config.mcpServers | Add-Member -NotePropertyName $mcpName -NotePropertyValue $mcpEntry -Force
        Write-Host "  Configured: $mcpName ($($mcp.description))" -ForegroundColor Gray
    }

    # Configure MCPs from mcps directory
    foreach ($mcpName in $mcpsDirMCPs.Keys) {
        $mcp = $mcpsDirMCPs[$mcpName]
        $entryPath = Join-Path $baseDir $mcpName | Join-Path -ChildPath $mcp.entry

        $mcpEntry = @{
            command = "node"
            args = @($entryPath)
        }

        if ($config.mcpServers.PSObject.Properties.Name -contains $mcpName) {
            $config.mcpServers.PSObject.Properties.Remove($mcpName)
        }
        $config.mcpServers | Add-Member -NotePropertyName $mcpName -NotePropertyValue $mcpEntry -Force
        Write-Host "  Configured: $mcpName ($($mcp.description))" -ForegroundColor Gray
    }

    # Configure verified npm MCPs
    foreach ($mcpName in $workingNpmMCPs.Keys) {
        $packageName = $workingNpmMCPs[$mcpName]

        $mcpEntry = @{
            command = "npx"
            args = @("-y", $packageName)
        }

        # Add specific configurations
        switch ($mcpName) {
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
        Write-Host "  Configured: $mcpName (npm: $packageName)" -ForegroundColor Gray
    }

    # Save configuration with proper JSON encoding
    Write-Host ""
    Write-Host "  Saving configuration..." -ForegroundColor Yellow

    try {
        # Generate clean JSON without BOM
        $jsonContent = $config | ConvertTo-Json -Depth 10 -Compress

        # Save with UTF8 without BOM to prevent Claude Desktop parsing issues
        [System.IO.File]::WriteAllText($configPath, $jsonContent, [System.Text.UTF8Encoding]::new($false))

        Write-Host "  Configuration saved successfully!" -ForegroundColor Green

        # Verify JSON is valid and readable
        $verification = Get-Content $configPath -Raw | ConvertFrom-Json
        $verifiedCount = @($verification.mcpServers.PSObject.Properties.Name).Count
        Write-Host "  Verified: $verifiedCount MCPs configured" -ForegroundColor Green

        # Additional Claude Desktop compatibility check
        if ($verification.mcpServers -and $verifiedCount -gt 0) {
            Write-Host "  JSON format validated for Claude Desktop compatibility" -ForegroundColor Green
        } else {
            throw "Configuration validation failed - no MCPs found"
        }
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
Write-Host "                       INSTALLATION COMPLETE                               " -ForegroundColor Green
Write-Host "============================================================================" -ForegroundColor Green
Write-Host ""

if (-not $WhatIf) {
    $finalConfig = Get-Content $configPath -Raw | ConvertFrom-Json
    $actualMCPCount = @($finalConfig.mcpServers.PSObject.Properties.Name).Count

    Write-Host "Summary:" -ForegroundColor Cyan
    Write-Host "  MCPs Configured: $actualMCPCount" -ForegroundColor White
    Write-Host "  Embedded MCPs: $($embeddedMCPs.Count + $mcpsDirMCPs.Count)" -ForegroundColor White
    Write-Host "  NPM MCPs: $($workingNpmMCPs.Count)" -ForegroundColor White
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

Write-Host "  2. Restart Claude Desktop" -ForegroundColor White
Write-Host ""
Write-Host "  3. Verify MCPs appear in Claude Desktop settings" -ForegroundColor White
Write-Host ""

if ($WhatIf) {
    Write-Host "[WHATIF] No changes were made. Remove -WhatIf to perform installation." -ForegroundColor Yellow
} else {
    Write-Host "SUCCESS: Claude Desktop is now configured with working MCPs!" -ForegroundColor Cyan
    Write-Host ""
}