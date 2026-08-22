$ErrorActionPreference = 'Stop'

$workflow = Join-Path $PSScriptRoot 'backend\printer_server\gstMonthlyWorkflow.js'
$node = (Get-Command node.exe -ErrorAction Stop).Source

Write-Host 'Starting the GST monthly workflow...'
& $node $workflow --manual @args
$exitCode = $LASTEXITCODE

if ($exitCode -eq 0) {
    Write-Host 'GST monthly workflow finished successfully.'
} else {
    Write-Error "GST monthly workflow failed with exit code $exitCode."
}

exit $exitCode
