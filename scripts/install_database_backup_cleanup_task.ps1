[CmdletBinding()]
param(
    [string]$TaskName = 'Hosangadi Database Backup Cleanup',
    [string]$ApplicationRoot,
    [string]$BackupDirectory = 'C:\backup',
    [int]$RetentionDays = 6,
    [switch]$Uninstall
)

#Requires -Version 5.1
#Requires -RunAsAdministrator

$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($ApplicationRoot)) {
    $ApplicationRoot = Split-Path $PSScriptRoot -Parent
}
$ApplicationRoot = [IO.Path]::GetFullPath($ApplicationRoot.Trim().Trim('"'))
$BackupDirectory = [IO.Path]::GetFullPath($BackupDirectory.Trim().Trim('"'))
$cleanupScript = Join-Path $ApplicationRoot 'scripts\cleanup_database_backups.ps1'
$powerShellPath = Join-Path $PSHOME 'powershell.exe'

$service = New-Object -ComObject 'Schedule.Service'
$service.Connect()
$rootFolder = $service.GetFolder('\')

if ($Uninstall) {
    try {
        $rootFolder.DeleteTask($TaskName, 0)
        Write-Host "Removed scheduled task: $TaskName"
    } catch {
        if ($_.Exception.Message -match 'cannot find|not exist') {
            Write-Host "Scheduled task was not installed: $TaskName"
        } else { throw }
    }
    exit 0
}

if ($RetentionDays -lt 1) { throw 'RetentionDays must be at least 1.' }
if (-not (Test-Path -LiteralPath $cleanupScript -PathType Leaf)) {
    throw "Backup cleanup script was not found: $cleanupScript"
}

$task = $service.NewTask(0)
$task.RegistrationInfo.Description = 'Deletes ordinary Hosangadi SQL backups older than six days while permanently preserving full financial-year backups.'
$task.Settings.Enabled = $true
$task.Settings.StartWhenAvailable = $true
$task.Settings.MultipleInstances = 2 # Ignore a new trigger while cleanup is running.
$task.Settings.ExecutionTimeLimit = 'PT30M'
$task.Settings.DisallowStartIfOnBatteries = $false
$task.Settings.StopIfGoingOnBatteries = $false

# TASK_TRIGGER_WEEKLY = 3. Sunday = 1 in the Task Scheduler day bitmask.
$weeklyTrigger = $task.Triggers.Create(3)
$weeklyTrigger.Enabled = $true
$weeklyTrigger.StartBoundary = (Get-Date).Date.AddDays(1).AddHours(3).ToString("yyyy-MM-dd'T'HH:mm:ss")
$weeklyTrigger.DaysOfWeek = 1
$weeklyTrigger.WeeksInterval = 1

$action = $task.Actions.Create(0)
$action.Path = $powerShellPath
$action.Arguments = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$cleanupScript`" -BackupDirectory `"$BackupDirectory`" -RetentionDays $RetentionDays"
$action.WorkingDirectory = Split-Path $cleanupScript -Parent

$task.Principal.UserId = 'SYSTEM'
$task.Principal.LogonType = 5
$task.Principal.RunLevel = 1

$null = $rootFolder.RegisterTaskDefinition($TaskName, $task, 6, 'SYSTEM', $null, 5, $null)

Write-Host "Installed or updated scheduled task: $TaskName"
Write-Host 'Schedule: every Sunday at 3:00 AM; a missed run starts when Windows is next available.'
Write-Host "Retention: completed SQL backups older than $RetentionDays days. aFullBackup_*.sql is always preserved."
Write-Host "Log: $(Join-Path $BackupDirectory 'backup-cleanup.log')"
