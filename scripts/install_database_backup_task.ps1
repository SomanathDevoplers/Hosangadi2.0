[CmdletBinding()]
param(
    [string]$TaskName = 'Hosangadi Database Backup',
    [string]$ApplicationRoot = (Split-Path $PSScriptRoot -Parent),
    [string]$BackupDirectory = 'C:\backup',
    [switch]$NoShutdownTrigger,
    [switch]$Uninstall
)

#Requires -Version 5.1
#Requires -RunAsAdministrator

$ErrorActionPreference = 'Stop'

# Normalize user-supplied paths before embedding them in Task Scheduler's
# command-line string. This also removes an accidentally retained quote after
# a directory argument ending in a backslash.
$ApplicationRoot = [IO.Path]::GetFullPath($ApplicationRoot.Trim().Trim('"'))
$BackupDirectory = [IO.Path]::GetFullPath($BackupDirectory.Trim().Trim('"'))

$backupScript = Join-Path $ApplicationRoot 'scripts\backup_databases.ps1'
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

if (-not (Test-Path -LiteralPath $backupScript -PathType Leaf)) {
    throw "Backup script was not found: $backupScript"
}

$task = $service.NewTask(0)
$task.RegistrationInfo.Description = 'Backs up the Hosangadi master and current financial-year MySQL databases at startup and every two hours.'
$task.Settings.Enabled = $true
$task.Settings.StartWhenAvailable = $true
$task.Settings.MultipleInstances = 2 # Ignore a new trigger while a backup is running.
$task.Settings.ExecutionTimeLimit = 'PT2H'
$task.Settings.DisallowStartIfOnBatteries = $false
$task.Settings.StopIfGoingOnBatteries = $false
$task.Settings.AllowHardTerminate = $false

# TASK_TRIGGER_BOOT = 8. Take one backup two minutes after every boot.
$bootTrigger = $task.Triggers.Create(8)
$bootTrigger.Enabled = $true
$bootTrigger.Delay = 'PT2M'

# TASK_TRIGGER_TIME = 1. Start two minutes after installation and repeat every
# two hours. Keeping repetition on a schedulable time trigger makes Task
# Scheduler calculate and display Next Run Time without waiting for a reboot.
$periodicTrigger = $task.Triggers.Create(1)
$periodicTrigger.Enabled = $true
$periodicTrigger.StartBoundary = (Get-Date).AddMinutes(2).ToString("yyyy-MM-dd'T'HH:mm:ss")
$periodicTrigger.Repetition.Interval = 'PT2H'
$periodicTrigger.Repetition.Duration = 'P9999D'
$periodicTrigger.Repetition.StopAtDurationEnd = $false

if (-not $NoShutdownTrigger) {
    # TASK_TRIGGER_EVENT = 0. User32 event 1074 is emitted when shutdown/restart is initiated.
    # This is best-effort: Windows may complete shutdown before a large dump finishes.
    $shutdownTrigger = $task.Triggers.Create(0)
    $shutdownTrigger.Enabled = $true
    $shutdownTrigger.Subscription = @'
<QueryList>
  <Query Id="0" Path="System">
    <Select Path="System">*[System[Provider[@Name='User32'] and EventID=1074]]</Select>
  </Query>
</QueryList>
'@
}

# TASK_ACTION_EXEC = 0.
$action = $task.Actions.Create(0)
$action.Path = $powerShellPath
$action.Arguments = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$backupScript`" -ApplicationRoot `"$ApplicationRoot`" -BackupDirectory `"$BackupDirectory`""
$action.WorkingDirectory = Split-Path $backupScript -Parent

# Run as Local System so the task works before logon and has no visible console.
$task.Principal.UserId = 'SYSTEM'
$task.Principal.LogonType = 5 # TASK_LOGON_SERVICE_ACCOUNT
$task.Principal.RunLevel = 1 # Highest privileges

# TASK_CREATE_OR_UPDATE = 6; TASK_LOGON_SERVICE_ACCOUNT = 5.
$null = $rootFolder.RegisterTaskDefinition($TaskName, $task, 6, 'SYSTEM', $null, 5, $null)

Write-Host "Installed or updated scheduled task: $TaskName"
Write-Host 'Schedule: once two minutes after startup, plus every two hours beginning two minutes after installation.'
if ($NoShutdownTrigger) {
    Write-Host 'Shutdown trigger: disabled.'
} else {
    Write-Warning 'Shutdown trigger enabled as best-effort only; the regular two-hour backups are authoritative.'
}
Write-Host "Backup destination: $BackupDirectory"
Write-Host "Log: $(Join-Path $BackupDirectory 'scheduled-backup.log')"
