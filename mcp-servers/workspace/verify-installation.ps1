# MCP Federation Core - Installation Verification Script
# This script checks if MCPs are ACTUALLY configured (not just claimed)

Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "              MCP FEDERATION CORE - INSTALLATION VERIFIER                   " -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"

# Expected Federation MCPs
$expectedMCPs = @(
    'sqlite',
    'expert-role-prompt',
    'kimi-k2-resilient-enhanced',
    'kimi-k2-code-context-enhanced',
    'rag-context',
    'converse',
    'web-search',
    'github-manager',
    'memory',
    'filesystem',
    'desktop-commander',
    'perplexity',
    'playwright',
    'git-ops',
    'sequential-thinking'
)

Write-Host "[CHECK 1] Configuration file exists..." -ForegroundColor Yellow

if (-not (Test-Path $configPath)) {
    Write-Host "  ❌ FAILED: Configuration file not found at: $configPath" -ForegroundColor Red
    Write-Host "  Claude Desktop may not be installed or config hasn't been created" -ForegroundColor Gray
    exit 1
} else {
    Write-Host "  ✅ PASSED: Configuration file exists" -ForegroundColor Green
}

Write-Host ""
Write-Host "[CHECK 2] Configuration file is valid JSON..." -ForegroundColor Yellow

try {
    $config = Get-Content $configPath -Raw | ConvertFrom-Json
    Write-Host "  ✅ PASSED: Valid JSON configuration" -ForegroundColor Green
} catch {
    Write-Host "  ❌ FAILED: Invalid JSON in configuration file" -ForegroundColor Red
    Write-Host "  Error: $_" -ForegroundColor Gray
    exit 1
}

Write-Host ""
Write-Host "[CHECK 3] MCPs are configured..." -ForegroundColor Yellow

if (-not $config.mcpServers) {
    Write-Host "  ❌ FAILED: No mcpServers section in configuration" -ForegroundColor Red
    Write-Host "  The installer did not configure any MCPs!" -ForegroundColor Red
    exit 1
}

$configuredMCPs = @($config.mcpServers.PSObject.Properties.Name)
$mcpCount = $configuredMCPs.Count

if ($mcpCount -eq 0) {
    Write-Host "  ❌ FAILED: No MCPs configured (count = 0)" -ForegroundColor Red
    Write-Host "  The installer claimed success but configured nothing!" -ForegroundColor Red
    exit 1
} else {
    Write-Host "  ✅ PASSED: Found $mcpCount configured MCPs" -ForegroundColor Green
}

Write-Host ""
Write-Host "[CHECK 4] Federation MCPs are present..." -ForegroundColor Yellow

$foundFederationMCPs = @()
$missingFederationMCPs = @()

foreach ($expectedMCP in $expectedMCPs) {
    if ($expectedMCP -in $configuredMCPs) {
        $foundFederationMCPs += $expectedMCP
    } else {
        $missingFederationMCPs += $expectedMCP
    }
}

if ($foundFederationMCPs.Count -eq 15) {
    Write-Host "  ✅ PASSED: All 15 Federation MCPs are configured!" -ForegroundColor Green
} elseif ($foundFederationMCPs.Count -gt 0) {
    Write-Host "  ⚠️  PARTIAL: Only $($foundFederationMCPs.Count) of 15 Federation MCPs found" -ForegroundColor Yellow
} else {
    Write-Host "  ❌ FAILED: No Federation MCPs found!" -ForegroundColor Red
}

Write-Host ""
Write-Host "[CHECK 5] MCP configurations have required fields..." -ForegroundColor Yellow

$validMCPs = 0
$invalidMCPs = @()

foreach ($mcpName in $configuredMCPs) {
    $mcp = $config.mcpServers.$mcpName

    if ($mcp.command -and $mcp.args) {
        $validMCPs++
    } else {
        $invalidMCPs += $mcpName
    }
}

if ($invalidMCPs.Count -eq 0) {
    Write-Host "  ✅ PASSED: All MCPs have required command and args fields" -ForegroundColor Green
} else {
    Write-Host "  ⚠️  WARNING: $($invalidMCPs.Count) MCPs missing required fields" -ForegroundColor Yellow
    foreach ($invalid in $invalidMCPs) {
        Write-Host "    - $invalid" -ForegroundColor Gray
    }
}

# Summary Report
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host "                            VERIFICATION SUMMARY                            " -ForegroundColor Cyan
Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""

Write-Host "Configuration Status:" -ForegroundColor White
Write-Host "  Config Path: $configPath" -ForegroundColor Gray
Write-Host "  Total MCPs: $mcpCount" -ForegroundColor Gray
Write-Host "  Federation MCPs: $($foundFederationMCPs.Count) / 15" -ForegroundColor Gray
Write-Host "  Valid Configs: $validMCPs / $mcpCount" -ForegroundColor Gray

if ($missingFederationMCPs.Count -gt 0) {
    Write-Host ""
    Write-Host "Missing Federation MCPs:" -ForegroundColor Yellow
    foreach ($missing in $missingFederationMCPs) {
        Write-Host "  ❌ $missing" -ForegroundColor Red
    }
}

if ($foundFederationMCPs.Count -gt 0) {
    Write-Host ""
    Write-Host "Found Federation MCPs:" -ForegroundColor Green
    foreach ($found in $foundFederationMCPs) {
        Write-Host "  ✅ $found" -ForegroundColor Green
    }
}

# Final Verdict
Write-Host ""
Write-Host "============================================================================" -ForegroundColor Cyan

if ($foundFederationMCPs.Count -eq 15) {
    Write-Host "       🎉 SUCCESS: MCP Federation Core is properly installed! 🎉" -ForegroundColor Green -BackgroundColor DarkGreen
} elseif ($foundFederationMCPs.Count -gt 0) {
    Write-Host "       ⚠️  PARTIAL: Some Federation MCPs are missing" -ForegroundColor Yellow -BackgroundColor DarkYellow
} else {
    Write-Host "       ❌ FAILURE: Installation did NOT configure MCPs!" -ForegroundColor Red -BackgroundColor DarkRed
    Write-Host ""
    Write-Host "The installer may have shown success messages but didn't actually work." -ForegroundColor Red
    Write-Host "Please use installer-fixed.ps1 instead of installer.ps1" -ForegroundColor Yellow
}

Write-Host "============================================================================" -ForegroundColor Cyan
Write-Host ""