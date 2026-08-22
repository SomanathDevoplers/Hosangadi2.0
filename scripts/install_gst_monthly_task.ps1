param(
    [string]$TaskName = 'Hosangadi GST Monthly Automation',
    [string]$ConfigPath,
    [switch]$Uninstall
)

$ErrorActionPreference = 'Stop'

$repositoryRoot = Split-Path $PSScriptRoot -Parent
$printerDirectory = Join-Path $repositoryRoot 'backend\printer_server'
$workflowPath = Join-Path $printerDirectory 'gstMonthlyWorkflow.js'
$exampleConfig = Join-Path $printerDirectory 'gst-monthly-automation.env.example'
$nodePath = (Get-Command node.exe -ErrorAction Stop).Source

if ([string]::IsNullOrWhiteSpace($ConfigPath)) {
    $ConfigPath = Join-Path $printerDirectory '.env'
}

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
        } else {
            throw
        }
    }
    exit 0
}

if (-not (Test-Path -LiteralPath $workflowPath)) {
    throw "Workflow entry point was not found: $workflowPath"
}

if (-not (Test-Path -LiteralPath $ConfigPath)) {
    $configDirectory = Split-Path $ConfigPath -Parent
    New-Item -ItemType Directory -Path $configDirectory -Force | Out-Null
    Copy-Item -LiteralPath $exampleConfig -Destination $ConfigPath
    Write-Warning "Created disabled configuration at $ConfigPath. Add the Gmail App Password and set GST_MONTHLY_AUTOMATION_ENABLED=true before the scheduled date."
}

$task = $service.NewTask(0)
$task.RegistrationInfo.Description = 'Generates and emails the previous month GST reports for SOMANATH STORES on the first Saturday at 10:00 AM.'
$task.Settings.Enabled = $true
$task.Settings.StartWhenAvailable = $true
$task.Settings.MultipleInstances = 2
$task.Settings.ExecutionTimeLimit = 'PT2H'
$task.Settings.DisallowStartIfOnBatteries = $false
$task.Settings.StopIfGoingOnBatteries = $false

# TASK_TRIGGER_MONTHLYDOW = 5. Saturday = 64, first week = 1, all months = 4095.
$trigger = $task.Triggers.Create(5)
$trigger.Enabled = $true
$trigger.StartBoundary = (Get-Date).Date.AddHours(10).ToString("yyyy-MM-dd'T'HH:mm:ss")
$trigger.DaysOfWeek = 64
$trigger.WeeksOfMonth = 1
$trigger.MonthsOfYear = 4095

# TASK_ACTION_EXEC = 0.
$action = $task.Actions.Create(0)
$action.Path = $nodePath
$action.Arguments = "`"$workflowPath`" --scheduled --config `"$ConfigPath`""
$action.WorkingDirectory = $printerDirectory

$currentUser = [Security.Principal.WindowsIdentity]::GetCurrent().Name
$task.Principal.UserId = $currentUser
$task.Principal.LogonType = 3
$task.Principal.RunLevel = 0

# TASK_CREATE_OR_UPDATE = 6; TASK_LOGON_INTERACTIVE_TOKEN = 3.
$null = $rootFolder.RegisterTaskDefinition($TaskName, $task, 6, $currentUser, $null, 3, $null)

Write-Host "Installed scheduled task: $TaskName"
Write-Host 'Schedule: first Saturday of every month at 10:00 AM'
Write-Host 'Missed-run recovery: enabled (runs when Task Scheduler next becomes available after user logon)'
Write-Host "Configuration: $ConfigPath"
