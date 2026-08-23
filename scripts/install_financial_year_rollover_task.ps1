[CmdletBinding()]
param(
    [string]$TaskName = 'Hosangadi Financial Year Rollover',
    [string]$ApplicationRoot = (Split-Path $PSScriptRoot -Parent),
    [string]$OperatorProfile = $env:USERPROFILE,
    [switch]$Uninstall
)

#Requires -Version 5.1
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'

# Normalize user-supplied paths before embedding them in Task Scheduler's
# command-line string. This also removes an accidentally retained quote after
# a directory argument ending in a backslash.
$ApplicationRoot = [IO.Path]::GetFullPath($ApplicationRoot.Trim().Trim('"'))
$OperatorProfile = [IO.Path]::GetFullPath($OperatorProfile.Trim().Trim('"'))

$service = New-Object -ComObject 'Schedule.Service'
$service.Connect()
$root = $service.GetFolder('\')
if ($Uninstall) {
    try { $root.DeleteTask($TaskName, 0) } catch { if ($_.Exception.Message -notmatch 'cannot find|not exist') { throw } }
    Write-Host "Removed scheduled task: $TaskName"
    exit 0
}

$rolloverScript = Join-Path $ApplicationRoot 'scripts\invoke_financial_year_rollover.ps1'
if (-not (Test-Path -LiteralPath $rolloverScript -PathType Leaf)) { throw "Rollover script was not found: $rolloverScript" }
$invoiceRoot = Join-Path $OperatorProfile 'Desktop\Invoices'

$task = $service.NewTask(0)
$task.RegistrationInfo.Description = 'Idempotent April 1 Hosangadi financial-year database and invoice rollover fallback.'
$task.Settings.Enabled = $true
$task.Settings.StartWhenAvailable = $true
$task.Settings.MultipleInstances = 2
$task.Settings.ExecutionTimeLimit = 'PT2H'
$task.Settings.DisallowStartIfOnBatteries = $false
$task.Settings.StopIfGoingOnBatteries = $false

# Annual calendar trigger: April 1 at 00:01. StartWhenAvailable runs a missed
# trigger when the computer next starts, so a separate every-boot trigger is unnecessary.
$trigger = $task.Triggers.Create(4) # TASK_TRIGGER_MONTHLY
$trigger.Enabled = $true
$nextAprilYear = if ((Get-Date) -lt (Get-Date -Month 4 -Day 1 -Hour 0 -Minute 1 -Second 0)) { (Get-Date).Year } else { (Get-Date).Year + 1 }
$trigger.StartBoundary = "$(Get-Date -Year $nextAprilYear -Month 4 -Day 1 -Hour 0 -Minute 1 -Second 0 -Format s)"
$trigger.DaysOfMonth = 1
$trigger.MonthsOfYear = 8 # April bitmask.

$action = $task.Actions.Create(0)
$action.Path = Join-Path $PSHOME 'powershell.exe'
$action.Arguments = "-NoProfile -NonInteractive -WindowStyle Hidden -ExecutionPolicy Bypass -File `"$rolloverScript`" -ApplicationRoot `"$ApplicationRoot`" -InvoiceRoot `"$invoiceRoot`""
$action.WorkingDirectory = Split-Path $rolloverScript -Parent
$task.Principal.UserId = 'SYSTEM'
$task.Principal.LogonType = 5
$task.Principal.RunLevel = 1
$null = $root.RegisterTaskDefinition($TaskName, $task, 6, 'SYSTEM', $null, 5, $null)

Write-Host "Installed scheduled task: $TaskName"
Write-Host 'Fallback: April 1 at 00:01; StartWhenAvailable handles a computer that was switched off.'
Write-Host "Invoice directory: $invoiceRoot"
Write-Warning 'Keep the login application closed until the rollover log reports COMPLETE.'
