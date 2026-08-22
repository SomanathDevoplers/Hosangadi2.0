[CmdletBinding()]
param(
    [string]$TaskName = 'Hosangadi Database Backup',
    [string]$ApplicationRoot = (Join-Path $env:USERPROFILE 'Hosangadi2.0'),
    [string]$BackupDirectory = 'C:\backup',
    [switch]$NoShutdownTrigger,
    [switch]$Uninstall
)

#Requires -Version 5.1
#Requires -RunAsAdministrator

$ErrorActionPreference = 'Stop'

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

# TASK_TRIGGER_BOOT = 8. Start two minutes after boot, then repeat every two hours.
$bootTrigger = $task.Triggers.Create(8)
$bootTrigger.Enabled = $true
$bootTrigger.Delay = 'PT2M'
$bootTrigger.Repetition.Interval = 'PT2H'
$bootTrigger.Repetition.Duration = 'P9999D'
$bootTrigger.Repetition.StopAtDurationEnd = $false

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
Write-Host 'Schedule: two minutes after startup, then every two hours while Windows remains running.'
if ($NoShutdownTrigger) {
    Write-Host 'Shutdown trigger: disabled.'
} else {
    Write-Warning 'Shutdown trigger enabled as best-effort only; the regular two-hour backups are authoritative.'
}
Write-Host "Backup destination: $BackupDirectory"
Write-Host "Log: $(Join-Path $BackupDirectory 'scheduled-backup.log')"

