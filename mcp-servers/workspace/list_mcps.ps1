$config = Get-Content 'C:\Users\User\AppData\Roaming\Claude\claude_desktop_config.json' | ConvertFrom-Json
$mcps = $config.mcpServers.PSObject.Properties.Name | Sort-Object
Write-Host "Total MCPs configured: $($mcps.Count)"
Write-Host ""
Write-Host "MCPs List:"
$i = 1
foreach ($mcp in $mcps) {
    Write-Host "  $i. $mcp"
    $i++
}