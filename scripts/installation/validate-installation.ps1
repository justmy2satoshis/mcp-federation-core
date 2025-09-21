# MCP Installation Validation Script

param(
    [string]$Environment = 'auto'
)

Write-Host "🔍 Validating MCP Installation..." -ForegroundColor Cyan
Write-Host ""

$RepoRoot = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
$validationResults = @{
    Passed = 0
    Failed = 0
    Warnings = 0
}

# Function to test a condition
function Test-Validation {
    param(
        [string]$Name,
        [scriptblock]$Test,
        [string]$SuccessMessage = "✓ $Name",
        [string]$FailureMessage = "❌ $Name"
    )

    try {
        $result = & $Test
        if ($result) {
            Write-Host $SuccessMessage -ForegroundColor Green
            $script:validationResults.Passed++
            return $true
        } else {
            Write-Host $FailureMessage -ForegroundColor Red
            $script:validationResults.Failed++
            return $false
        }
    } catch {
        Write-Host "$FailureMessage : $_" -ForegroundColor Red
        $script:validationResults.Failed++
        return $false
    }
}

# 1. Check directory structure
Write-Host "Directory Structure:" -ForegroundColor Yellow
Test-Validation -Name "MCPs directory exists" -Test {
    Test-Path "$RepoRoot\mcps"
}

Test-Validation -Name "Configs directory exists" -Test {
    Test-Path "$RepoRoot\configs"
}

Test-Validation -Name "Scripts directory exists" -Test {
    Test-Path "$RepoRoot\scripts"
}

Test-Validation -Name "Databases directory exists" -Test {
    Test-Path "$RepoRoot\databases"
}

Write-Host ""

# 2. Check MCP binaries
Write-Host "MCP Binaries:" -ForegroundColor Yellow
$requiredMcps = @(
    "expert-role-prompt",
    "kimi-k2-resilient-enhanced",
    "kimi-k2-code-context-enhanced"
)

foreach ($mcp in $requiredMcps) {
    Test-Validation -Name "$mcp exists" -Test {
        Test-Path "$RepoRoot\mcps\$mcp"
    }
}

Write-Host ""

# 3. Check runtime dependencies
Write-Host "Runtime Dependencies:" -ForegroundColor Yellow
Test-Validation -Name "Node.js installed" -Test {
    Get-Command node -ErrorAction SilentlyContinue
}

Test-Validation -Name "Python installed" -Test {
    Get-Command python -ErrorAction SilentlyContinue
}

Test-Validation -Name "npm installed" -Test {
    Get-Command npm -ErrorAction SilentlyContinue
}

Write-Host ""

# 4. Check configurations
Write-Host "Configurations:" -ForegroundColor Yellow

if ($Environment -eq 'auto') {
    $hasClaudeCode = Get-Command claude -ErrorAction SilentlyContinue
    $hasClaudeDesktop = Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"

    if ($hasClaudeCode -and $hasClaudeDesktop) {
        $Environment = 'both'
    } elseif ($hasClaudeCode) {
        $Environment = 'code'
    } elseif ($hasClaudeDesktop) {
        $Environment = 'desktop'
    }
}

if ($Environment -eq 'desktop' -or $Environment -eq 'both') {
    Test-Validation -Name "Claude Desktop config exists" -Test {
        Test-Path "$env:APPDATA\Claude\claude_desktop_config.json"
    }

    # Count MCPs in Desktop config
    if (Test-Path "$env:APPDATA\Claude\claude_desktop_config.json") {
        $desktopConfig = Get-Content "$env:APPDATA\Claude\claude_desktop_config.json" | ConvertFrom-Json
        $mcpCount = ($desktopConfig.mcpServers | Get-Member -MemberType NoteProperty).Count
        if ($mcpCount -ge 15) {
            Write-Host "  ✓ Claude Desktop has $mcpCount MCPs configured" -ForegroundColor Green
            $validationResults.Passed++
        } else {
            Write-Host "  ⚠ Claude Desktop has only $mcpCount MCPs (expected 15+)" -ForegroundColor Yellow
            $validationResults.Warnings++
        }
    }
}

if ($Environment -eq 'code' -or $Environment -eq 'both') {
    Test-Validation -Name "Claude Code CLI available" -Test {
        Get-Command claude -ErrorAction SilentlyContinue
    }

    # Test MCP list command
    if (Get-Command claude -ErrorAction SilentlyContinue) {
        try {
            $mcpList = claude mcp list 2>$null
            $connectedCount = ($mcpList | Select-String "Connected").Count
            if ($connectedCount -ge 15) {
                Write-Host "  ✓ Claude Code has $connectedCount MCPs connected" -ForegroundColor Green
                $validationResults.Passed++
            } else {
                Write-Host "  ⚠ Claude Code has only $connectedCount MCPs connected (expected 15+)" -ForegroundColor Yellow
                $validationResults.Warnings++
            }
        } catch {
            Write-Host "  ❌ Could not list Claude Code MCPs" -ForegroundColor Red
            $validationResults.Failed++
        }
    }
}

Write-Host ""

# 5. Check template files
Write-Host "Template Files:" -ForegroundColor Yellow
Test-Validation -Name "Desktop config template exists" -Test {
    Test-Path "$RepoRoot\configs\templates\claude-desktop-config.template.json"
}

Test-Validation -Name "Code config template exists" -Test {
    Test-Path "$RepoRoot\configs\templates\claude-code-config.template.json"
}

Test-Validation -Name "Environment template exists" -Test {
    Test-Path "$RepoRoot\.env.template"
}

Write-Host ""

# 6. Check for .env file
Write-Host "Environment Configuration:" -ForegroundColor Yellow
if (Test-Path "$RepoRoot\.env") {
    Write-Host "  ✓ .env file exists" -ForegroundColor Green
    $validationResults.Passed++

    # Check for API keys
    $envContent = Get-Content "$RepoRoot\.env"
    $apiKeys = @("OPENAI_API_KEY", "PERPLEXITY_API_KEY", "GITHUB_PERSONAL_ACCESS_TOKEN", "BRAVE_API_KEY")
    $missingKeys = @()

    foreach ($key in $apiKeys) {
        if (-not ($envContent | Select-String "$key=.+")) {
            $missingKeys += $key
        }
    }

    if ($missingKeys.Count -eq 0) {
        Write-Host "  ✓ All API keys configured" -ForegroundColor Green
        $validationResults.Passed++
    } else {
        Write-Host "  ⚠ Missing API keys: $($missingKeys -join ', ')" -ForegroundColor Yellow
        $validationResults.Warnings++
    }
} else {
    Write-Host "  ⚠ No .env file found (copy from .env.template)" -ForegroundColor Yellow
    $validationResults.Warnings++
}

Write-Host ""

# 7. Check Git repository
Write-Host "Git Repository:" -ForegroundColor Yellow
Test-Validation -Name "Git repository initialized" -Test {
    Test-Path "$RepoRoot\.git"
}

if (Test-Path "$RepoRoot\.git") {
    Push-Location $RepoRoot
    $gitStatus = git status --porcelain 2>$null
    if (-not $gitStatus) {
        Write-Host "  ✓ Working tree clean" -ForegroundColor Green
        $validationResults.Passed++
    } else {
        Write-Host "  ⚠ Uncommitted changes in repository" -ForegroundColor Yellow
        $validationResults.Warnings++
    }
    Pop-Location
}

Write-Host ""
Write-Host "═══════════════════════════════════════════════" -ForegroundColor Cyan
Write-Host "Validation Summary:" -ForegroundColor White
Write-Host "  ✓ Passed: $($validationResults.Passed)" -ForegroundColor Green
if ($validationResults.Warnings -gt 0) {
    Write-Host "  ⚠ Warnings: $($validationResults.Warnings)" -ForegroundColor Yellow
}
if ($validationResults.Failed -gt 0) {
    Write-Host "  ❌ Failed: $($validationResults.Failed)" -ForegroundColor Red
}

if ($validationResults.Failed -eq 0) {
    Write-Host ""
    Write-Host "✅ Installation validation successful!" -ForegroundColor Green
    exit 0
} else {
    Write-Host ""
    Write-Host "❌ Installation validation failed. Please review the errors above." -ForegroundColor Red
    exit 1
}