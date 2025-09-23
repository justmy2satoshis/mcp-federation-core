# MCP Federation Diagnostic Script
# Checks current state and identifies issues

Write-Host ""
Write-Host "=== MCP FEDERATION DIAGNOSTIC ===" -ForegroundColor Cyan
Write-Host ""

# Check Claude Desktop config
Write-Host "[CONFIG CHECK]" -ForegroundColor Yellow
$configPath = "$env:APPDATA\Claude\claude_desktop_config.json"

if (Test-Path $configPath) {
    Write-Host "  ✓ Config file exists" -ForegroundColor Green

    try {
        $config = Get-Content $configPath -Raw | ConvertFrom-Json
        Write-Host "  ✓ JSON is valid" -ForegroundColor Green

        if ($config.mcpServers) {
            $mcpCount = @($config.mcpServers.PSObject.Properties.Name).Count
            Write-Host "  ✓ Found $mcpCount MCPs configured" -ForegroundColor Green
        } else {
            Write-Host "  ✗ No MCPs configured" -ForegroundColor Red
        }
    }
    catch {
        Write-Host "  ✗ JSON parsing error: $_" -ForegroundColor Red
    }
} else {
    Write-Host "  ✗ Config file not found" -ForegroundColor Red
}

# Check MCP directories
Write-Host ""
Write-Host "[DIRECTORY CHECK]" -ForegroundColor Yellow
$baseDir = "$env:USERPROFILE\mcp-servers"

if (Test-Path $baseDir) {
    Write-Host "  ✓ Base directory exists: $baseDir" -ForegroundColor Green
} else {
    Write-Host "  ✗ Base directory missing: $baseDir" -ForegroundColor Red
}

# Check specific MCPs
Write-Host ""
Write-Host "[MCP IMPLEMENTATION CHECK]" -ForegroundColor Yellow

if ($config.mcpServers) {
    $missingCount = 0
    $workingCount = 0

    foreach ($mcpName in $config.mcpServers.PSObject.Properties.Name) {
        $mcp = $config.mcpServers.$mcpName

        Write-Host ""
        Write-Host "  ${mcpName}:" -ForegroundColor White
        Write-Host "    Command: $($mcp.command)" -ForegroundColor Gray

        # Check based on command type
        switch ($mcp.command) {
            "node" {
                $scriptPath = $mcp.args[0]
                if (Test-Path $scriptPath) {
                    Write-Host "    ✓ Script exists: $scriptPath" -ForegroundColor Green
                    $workingCount++
                } else {
                    Write-Host "    ✗ Script missing: $scriptPath" -ForegroundColor Red
                    $missingCount++
                }
            }
            "npx" {
                # NPX packages are downloaded on demand
                Write-Host "    ℹ NPX package: $($mcp.args[1])" -ForegroundColor Cyan
                Write-Host "    (Will be downloaded when first used)" -ForegroundColor Gray
                $workingCount++
            }
            "python" {
                $module = $mcp.args[1]
                Write-Host "    Python module: $module" -ForegroundColor Cyan

                # Try to check if module is installed
                $checkCmd = "python -c `"import $module`" 2>&1"
                $result = Invoke-Expression $checkCmd
                if ($LASTEXITCODE -eq 0) {
                    Write-Host "    ✓ Module installed" -ForegroundColor Green
                    $workingCount++
                } else {
                    Write-Host "    ✗ Module not installed" -ForegroundColor Red
                    $missingCount++
                }
            }
        }
    }

    Write-Host ""
    Write-Host "[SUMMARY]" -ForegroundColor Yellow
    Write-Host "  Working MCPs: $workingCount" -ForegroundColor Green
    Write-Host "  Missing MCPs: $missingCount" -ForegroundColor Red
}

# Check Claude Desktop process
Write-Host ""
Write-Host "[CLAUDE DESKTOP CHECK]" -ForegroundColor Yellow
$claudeProcesses = Get-Process -Name "claude" -ErrorAction SilentlyContinue

if ($claudeProcesses) {
    Write-Host "  ✓ Claude Desktop is running ($($claudeProcesses.Count) processes)" -ForegroundColor Green
    Write-Host "  ℹ Restart required after configuration changes" -ForegroundColor Cyan
} else {
    Write-Host "  ℹ Claude Desktop is not running" -ForegroundColor Yellow
}

# Prerequisites check
Write-Host ""
Write-Host "[PREREQUISITES CHECK]" -ForegroundColor Yellow

@(
    @{Name="Python"; Command="python --version"},
    @{Name="Node.js"; Command="node --version"},
    @{Name="Git"; Command="git --version"},
    @{Name="npm"; Command="npm --version"}
) | ForEach-Object {
    try {
        $output = Invoke-Expression $_.Command 2>&1
        Write-Host "  ✓ $($_.Name): $output" -ForegroundColor Green
    }
    catch {
        Write-Host "  ✗ $($_.Name) not found" -ForegroundColor Red
    }
}

# Recommendations
Write-Host ""
Write-Host "[RECOMMENDATIONS]" -ForegroundColor Yellow

if ($missingCount -gt 0) {
    Write-Host "  1. Run the complete installer to download missing MCPs:" -ForegroundColor White
    Write-Host "     .\installer-complete-fixed.ps1" -ForegroundColor Cyan
}

Write-Host "  2. Configure API keys in:" -ForegroundColor White
Write-Host "     $configPath" -ForegroundColor Cyan

Write-Host "  3. Restart Claude Desktop after making changes" -ForegroundColor White

Write-Host ""