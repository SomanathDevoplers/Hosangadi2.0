[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$ApplicationRoot,

    [string]$BackupDirectory = 'C:\backup'
)

$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$mutex = New-Object Threading.Mutex($false, 'Global\HosangadiDatabaseBackup')
$hasMutex = $false

try {
    $hasMutex = $mutex.WaitOne(0)
    if (-not $hasMutex) {
        # A startup/two-hour/shutdown invocation is already producing a backup.
        exit 0
    }

    if (-not (Test-Path -LiteralPath $BackupDirectory -PathType Container)) {
        New-Item -ItemType Directory -Path $BackupDirectory -Force | Out-Null
    }

    $mysqlDump = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe'
    if (-not (Test-Path -LiteralPath $mysqlDump -PathType Leaf)) {
        throw "mysqldump.exe was not found at $mysqlDump"
    }

    $runtimeConfig = Join-Path $ApplicationRoot 'backend\printer_server\gstRuntimeConfig.js'
    if (-not (Test-Path -LiteralPath $runtimeConfig -PathType Leaf)) {
        throw "Database configuration was not found: $runtimeConfig"
    }

    $configText = Get-Content -Raw -LiteralPath $runtimeConfig
    if ($configText -notmatch "(?m)^\s*password:\s*'([^']+)'\s*$") {
        throw 'Could not read the legacy database password contract.'
    }
    $databasePassword = $Matches[1]

    $now = Get-Date
    $financialYearStart = if ($now.Month -lt 4) { $now.Year - 1 } else { $now.Year }
    $yearDatabase = "somanath$financialYearStart"
    $timestamp = $now.ToString('yyyy-MM-dd_HH-mm-ss')
    $finalPath = Join-Path $BackupDirectory "somanathstores_$timestamp.sql"
    $temporaryPath = "$finalPath.partial"
    $logPath = Join-Path $BackupDirectory 'scheduled-backup.log'

    $env:MYSQL_PWD = $databasePassword
    try {
        $arguments = @(
            '--host=localhost',
            '--port=3306',
            '--user=root',
            '--single-transaction',
            '--routines',
            '--triggers',
            '--events',
            '--databases',
            'somanath',
            $yearDatabase
        )
        $process = Start-Process -FilePath $mysqlDump -ArgumentList $arguments `
            -RedirectStandardOutput $temporaryPath -RedirectStandardError "$temporaryPath.error" `
            -WindowStyle Hidden -Wait -PassThru

        if ($process.ExitCode -ne 0) {
            $details = if (Test-Path -LiteralPath "$temporaryPath.error") {
                (Get-Content -Raw -LiteralPath "$temporaryPath.error").Trim()
            } else { 'No mysqldump error text was produced.' }
            throw "mysqldump failed with exit code $($process.ExitCode): $details"
        }
        if (-not (Test-Path -LiteralPath $temporaryPath) -or (Get-Item -LiteralPath $temporaryPath).Length -eq 0) {
            throw 'mysqldump produced an empty backup.'
        }

        Move-Item -LiteralPath $temporaryPath -Destination $finalPath -Force
        Remove-Item -LiteralPath "$temporaryPath.error" -Force -ErrorAction SilentlyContinue
        Add-Content -LiteralPath $logPath -Value "$(Get-Date -Format s) SUCCESS $yearDatabase $finalPath"
    } finally {
        $databasePassword = $null
        Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue
    }
} catch {
    if ($BackupDirectory) {
        New-Item -ItemType Directory -Path $BackupDirectory -Force -ErrorAction SilentlyContinue | Out-Null
        Add-Content -LiteralPath (Join-Path $BackupDirectory 'scheduled-backup.log') `
            -Value "$(Get-Date -Format s) ERROR $($_.Exception.Message)" -ErrorAction SilentlyContinue
    }
    exit 1
} finally {
    if ($hasMutex) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
}

