[CmdletBinding()]
param(
    [Parameter(Mandatory)]
    [string]$BackupFolder,

    [string]$ApplicationRoot = (Join-Path $env:USERPROFILE 'Hosangadi2.0')
)

#Requires -Version 5.1
#Requires -RunAsAdministrator
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$databasePassword = $null

function Get-DumpSchemas([string]$Path) {
    return @(
        Select-String -LiteralPath $Path -Pattern '(?i)^\s*USE\s+`?([a-z0-9_]+)`?\s*;' -AllMatches |
            ForEach-Object { $_.Matches } |
            ForEach-Object { $_.Groups[1].Value.ToLowerInvariant() } |
            Where-Object { $_ -match '^somanath(?:20\d{2,4})?$' } |
            Sort-Object -Unique
    )
}

function Invoke-MySql([string]$Sql) {
    $output = (& $script:mysqlPath --host=localhost --port=3306 --user=root --batch --skip-column-names --execute=$Sql 2>&1 | Out-String).Trim()
    if ($LASTEXITCODE -ne 0) { throw "mysql failed: $output" }
    return $output
}

try {
    $BackupFolder = [IO.Path]::GetFullPath($BackupFolder.Trim().Trim('"'))
    $ApplicationRoot = [IO.Path]::GetFullPath($ApplicationRoot.Trim().Trim('"'))
    if (-not (Test-Path -LiteralPath $BackupFolder -PathType Container)) { throw "Backup folder does not exist: $BackupFolder" }

    $sqlFiles = @(Get-ChildItem -LiteralPath $BackupFolder -Filter '*.sql' -File)
    if ($sqlFiles.Count -ne 2) {
        throw "Exactly two completed .sql files must be beside restore_backup_system.bat. Found $($sqlFiles.Count) in $BackupFolder. Remove unrelated SQL files and do not rename .partial files."
    }
    $orderedFiles = @($sqlFiles | Sort-Object Length)
    $latestFile = $orderedFiles[0]
    $fullFile = $orderedFiles[1]
    if ($latestFile.Length -le 0 -or $fullFile.Length -le $latestFile.Length) {
        throw 'Both SQL files must be non-empty and the full backup must be larger than the latest two-database backup.'
    }

    $latestSchemas = @(Get-DumpSchemas $latestFile.FullName)
    $fullSchemas = @(Get-DumpSchemas $fullFile.FullName)
    $latestYearSchemas = @($latestSchemas | Where-Object { $_ -match '^somanath20\d{2,4}$' })
    if ($latestSchemas.Count -ne 2 -or $latestSchemas -notcontains 'somanath' -or $latestYearSchemas.Count -ne 1) {
        throw "Smaller SQL file must contain exactly somanath plus one somanath20YY database. File: $($latestFile.Name); found: $($latestSchemas -join ', ')"
    }
    if ($fullSchemas.Count -le 2 -or $fullSchemas -notcontains 'somanath') {
        throw "Larger SQL file must contain somanath plus more than one financial-year database. File: $($fullFile.Name); found: $($fullSchemas -join ', ')"
    }

    Write-Host ''
    Write-Host 'Validated emergency restore files:' -ForegroundColor Cyan
    Write-Host "  Full history first : $($fullFile.FullName) ($($fullFile.Length) bytes)"
    Write-Host "  Latest data second : $($latestFile.FullName) ($($latestFile.Length) bytes)"
    Write-Host "  Full schemas       : $($fullSchemas -join ', ')"
    Write-Host "  Latest schemas     : $($latestSchemas -join ', ')"
    Write-Warning 'This operation permanently drops every existing somanath/somanath20YY database on this computer, restores the full dump, then overwrites master + current FY with the latest dump.'
    if ((Read-Host 'Type RESTORE to continue') -cne 'RESTORE') { throw 'Confirmation was not entered. No databases were changed.' }

    $script:mysqlPath = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
    if (-not (Test-Path -LiteralPath $script:mysqlPath -PathType Leaf)) { throw "mysql.exe was not found: $script:mysqlPath" }
    $runtimeConfig = Join-Path $ApplicationRoot 'backend\printer_server\gstRuntimeConfig.js'
    if (-not (Test-Path -LiteralPath $runtimeConfig -PathType Leaf)) { throw "Deployed database configuration was not found: $runtimeConfig" }
    $configText = Get-Content -Raw -LiteralPath $runtimeConfig
    $passwordMatch = [regex]::Match($configText, "(?m)^\s*password:\s*'([^']+)'\s*$")
    if (-not $passwordMatch.Success) { throw 'Could not read the legacy database password contract.' }
    $databasePassword = $passwordMatch.Groups[1].Value
    $env:MYSQL_PWD = $databasePassword
    Invoke-MySql 'SELECT 1;' | Out-Null

    $machinePath = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $userPath = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$machinePath;$userPath"
    $pm2 = Get-Command pm2.cmd -ErrorAction SilentlyContinue
    if ($pm2) {
        & $pm2.Source stop all
        if ($LASTEXITCODE -ne 0) { throw 'Could not stop PM2 applications before database replacement.' }
    } else {
        Write-Warning 'pm2.cmd was not found; ensure no Hosangadi backend process is running during restore.'
    }

    $applicationPorts = @(4000, 5000, 6000, 7000, 8000)
    $listeningPorts = @()
    for ($attempt = 0; $attempt -lt 10; $attempt++) {
        $listeningPorts = @(Get-NetTCPConnection -State Listen -ErrorAction SilentlyContinue |
            Where-Object { $applicationPorts -contains $_.LocalPort } |
            Select-Object -ExpandProperty LocalPort -Unique)
        if (-not $listeningPorts.Count) { break }
        Start-Sleep -Seconds 1
    }
    if ($listeningPorts.Count) {
        throw "Hosangadi ports are still listening after the stop attempt: $($listeningPorts -join ', '). No databases were dropped."
    }

    $existingOutput = Invoke-MySql "SELECT schema_name FROM information_schema.schemata WHERE schema_name='somanath' OR schema_name REGEXP '^somanath20[0-9]{2,4}$' ORDER BY schema_name;"
    $existingSchemas = @($existingOutput -split '\r?\n' | Where-Object { $_ -match '^somanath(?:20\d{2,4})?$' })
    foreach ($schema in $existingSchemas) {
        Write-Host "Dropping existing database: $schema"
        Invoke-MySql "DROP DATABASE IF EXISTS ``$schema``;" | Out-Null
    }

    foreach ($restoreFile in @($fullFile, $latestFile)) {
        $sourcePath = $restoreFile.FullName.Replace('\', '/')
        Write-Host "Restoring: $($restoreFile.Name)"
        Invoke-MySql "source $sourcePath" | Out-Null
    }

    $expectedSchemas = @(($fullSchemas + $latestSchemas) | Sort-Object -Unique)
    $restoredOutput = Invoke-MySql "SELECT schema_name FROM information_schema.schemata WHERE schema_name='somanath' OR schema_name REGEXP '^somanath20[0-9]{2,4}$' ORDER BY schema_name;"
    $restoredSchemas = @($restoredOutput -split '\r?\n' | Where-Object { $_ -match '^somanath(?:20\d{2,4})?$' })
    $missingSchemas = @($expectedSchemas | Where-Object { $restoredSchemas -notcontains $_ })
    if ($missingSchemas.Count) { throw "Restore finished but expected schemas are missing: $($missingSchemas -join ', ')" }
    foreach ($schema in $expectedSchemas) {
        $tableCount = [int](Invoke-MySql "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$schema';")
        if ($tableCount -eq 0) { throw "Restored database has no tables: $schema" }
    }

    if ($pm2) {
        $ecosystem = Join-Path $ApplicationRoot 'backend\ecosystem.config.js'
        if (-not (Test-Path -LiteralPath $ecosystem -PathType Leaf)) { throw "PM2 ecosystem file was not found: $ecosystem" }
        & $pm2.Source startOrReload $ecosystem --update-env
        if ($LASTEXITCODE -ne 0) { throw 'Database restore succeeded, but PM2 applications could not be restarted.' }
        & $pm2.Source save
        if ($LASTEXITCODE -ne 0) { throw 'Applications restarted, but PM2 save failed.' }
    }

    Write-Host ''
    Write-Host "Restore complete. Databases: $($restoredSchemas -join ', ')" -ForegroundColor Green
} catch {
    Write-Error -ErrorRecord $_
    exit 1
} finally {
    $databasePassword = $null
    Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue
}
