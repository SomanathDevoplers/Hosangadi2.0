[CmdletBinding()]
param(
    [string]$BackupDirectory = 'C:\backup',
    [int]$RetentionDays = 6
)

#Requires -Version 5.1

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

if ($RetentionDays -lt 1) { throw 'RetentionDays must be at least 1.' }

$BackupDirectory = [IO.Path]::GetFullPath($BackupDirectory.Trim().Trim('"'))
if (-not (Test-Path -LiteralPath $BackupDirectory -PathType Container)) {
    New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
}

$cutoff = (Get-Date).AddDays(-$RetentionDays)
$logPath = Join-Path $BackupDirectory 'backup-cleanup.log'
$deletedCount = 0
$deletedBytes = [long]0

try {
    foreach ($file in @(Get-ChildItem -LiteralPath $BackupDirectory -File -Filter '*.sql')) {
        # Financial-year safety backups are permanent and must never be aged out.
        if ($file.Name -like 'aFullBackup_*.sql') { continue }
        if ($file.CreationTime -ge $cutoff) { continue }

        $deletedBytes += $file.Length
        Remove-Item -LiteralPath $file.FullName -Force
        $deletedCount++
        Add-Content -LiteralPath $logPath -Encoding UTF8 -Value (
            '{0:u} DELETED name="{1}" created={2:u} bytes={3}' -f (Get-Date), $file.Name, $file.CreationTime, $file.Length
        )
    }
    Add-Content -LiteralPath $logPath -Encoding UTF8 -Value (
        '{0:u} SUCCESS cutoff={1:u} deleted={2} bytes={3}' -f (Get-Date), $cutoff, $deletedCount, $deletedBytes
    )
} catch {
    Add-Content -LiteralPath $logPath -Encoding UTF8 -Value (
        '{0:u} ERROR {1}' -f (Get-Date), $_.Exception.Message
    )
    throw
}

