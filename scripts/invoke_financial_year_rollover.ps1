[CmdletBinding()]
param(
    [string]$ApplicationRoot,
    [string]$InvoiceRoot = (Join-Path $env:USERPROFILE 'Desktop\Invoices'),
    [switch]$Force
)

#Requires -Version 5.1
$ErrorActionPreference = 'Stop'

if ([string]::IsNullOrWhiteSpace($ApplicationRoot)) {
    $ApplicationRoot = Split-Path $PSScriptRoot -Parent
}
Set-StrictMode -Version 2.0

$mutex = New-Object Threading.Mutex($false, 'Global\HosangadiFinancialYearRollover')
$hasMutex = $false
$backupMutex = New-Object Threading.Mutex($false, 'Global\HosangadiDatabaseBackup')
$hasBackupMutex = $false
$databasePassword = $null
$logDirectory = Join-Path $env:ProgramData 'Hosangadi'
$logPath = Join-Path $logDirectory 'financial-year-rollover.log'

function Write-RolloverLog([string]$Message) {
    New-Item -ItemType Directory -Path $logDirectory -Force | Out-Null
    Add-Content -LiteralPath $logPath -Value "$(Get-Date -Format s) $Message"
}

function Invoke-MySql([string]$Sql) {
    $start = New-Object Diagnostics.ProcessStartInfo
    $start.FileName = $script:mysqlExe
    $start.Arguments = '--host=localhost --port=3306 --user=root --batch --skip-column-names'
    $start.UseShellExecute = $false
    $start.CreateNoWindow = $true
    $start.RedirectStandardInput = $true
    $start.RedirectStandardOutput = $true
    $start.RedirectStandardError = $true
    $process = New-Object Diagnostics.Process
    $process.StartInfo = $start
    $null = $process.Start()
    $process.StandardInput.WriteLine($Sql)
    $process.StandardInput.Close()
    $output = $process.StandardOutput.ReadToEnd().Trim()
    $errorText = $process.StandardError.ReadToEnd().Trim()
    $process.WaitForExit()
    if ($process.ExitCode -ne 0) { throw "mysql failed: $errorText" }
    return $output
}

function Get-ArchiveFileDestination([string]$Source, [string]$Destination, [switch]$WarnOnDifference) {
    if (-not (Test-Path -LiteralPath $Destination)) { return $Destination }
    $sourceItem = Get-Item -LiteralPath $Source -Force
    $destinationItem = Get-Item -LiteralPath $Destination -Force
    if ($destinationItem.PSIsContainer) { throw "Invoice archive type collision: $Destination" }
    $sourceHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $Source).Hash
    if ($sourceItem.Length -eq $destinationItem.Length -and $sourceHash -eq (Get-FileHash -Algorithm SHA256 -LiteralPath $Destination).Hash) {
        return $Destination
    }
    if ($WarnOnDifference) {
        Write-Warning "Skipping different same-name invoice file; source left unchanged: $Source (archive already has $Destination)"
    }
    return $null
}

function Test-ArchiveMerge([string]$Source, [string]$Destination) {
    if (-not (Test-Path -LiteralPath $Destination)) { return }
    $sourceItem = Get-Item -LiteralPath $Source -Force
    $destinationItem = Get-Item -LiteralPath $Destination -Force
    if ($sourceItem.PSIsContainer -ne $destinationItem.PSIsContainer) {
        throw "Invoice archive type collision: $Destination"
    }
    if (-not $sourceItem.PSIsContainer) {
        $null = Get-ArchiveFileDestination -Source $Source -Destination $Destination
        return
    }
    foreach ($child in @(Get-ChildItem -LiteralPath $Source -Force)) {
        Test-ArchiveMerge -Source $child.FullName -Destination (Join-Path $Destination $child.Name)
    }
}

function Merge-ArchiveItem([string]$Source, [string]$Destination) {
    if (-not (Test-Path -LiteralPath $Destination)) {
        Move-Item -LiteralPath $Source -Destination $Destination
        return
    }
    $sourceItem = Get-Item -LiteralPath $Source -Force
    if (-not $sourceItem.PSIsContainer) {
        $fileDestination = Get-ArchiveFileDestination -Source $Source -Destination $Destination -WarnOnDifference
        if ([string]::IsNullOrWhiteSpace($fileDestination)) { return }
        if (Test-Path -LiteralPath $fileDestination) {
            # Preflight proved this exact content is already archived.
            Remove-Item -LiteralPath $Source -Force
        } else {
            Move-Item -LiteralPath $Source -Destination $fileDestination
        }
        return
    }
    foreach ($child in @(Get-ChildItem -LiteralPath $Source -Force)) {
        Merge-ArchiveItem -Source $child.FullName -Destination (Join-Path $Destination $child.Name)
    }
    if (@(Get-ChildItem -LiteralPath $Source -Force).Count -eq 0) {
        Remove-Item -LiteralPath $Source -Force
    } else {
        Write-Warning "Source invoice directory retained because it contains skipped conflicts: $Source"
    }
}

try {
    $hasMutex = $mutex.WaitOne(0)
    if (-not $hasMutex) { exit 0 }

    # A quoted Windows command-line argument ending in a backslash can retain
    # its closing quote. Normalize both roots before using them with Join-Path.
    $ApplicationRoot = [IO.Path]::GetFullPath($ApplicationRoot.Trim().Trim('"'))
    $InvoiceRoot = [IO.Path]::GetFullPath($InvoiceRoot.Trim().Trim('"'))

    $now = Get-Date
    if (-not $Force -and -not (($now.Month -eq 3 -and $now.Day -eq 31) -or ($now.Month -eq 4 -and $now.Day -eq 1))) {
        throw 'Financial-year rollover may run only on March 31 or April 1. Use -Force only for a controlled recovery/test.'
    }

    $targetYear = if ($now.Month -le 3) { $now.Year } else { $now.Year }
    $sourceYear = $targetYear - 1
    $sourceDatabase = "somanath$sourceYear"
    $targetDatabase = "somanath$targetYear"
    $sourceShort = ([string]$sourceYear).Substring(2, 2)
    $targetShort = ([string]$targetYear).Substring(2, 2)
    $archiveName = "z$sourceShort-$targetShort"

    $oldInvoices = Join-Path $InvoiceRoot 'oldinvoices'
    $archivePath = Join-Path $oldInvoices $archiveName
    New-Item -ItemType Directory -Path $archivePath -Force | Out-Null
    $archiveItems = @(Get-ChildItem -LiteralPath $oldInvoices -Force | Where-Object { $_.Name -ne $archiveName })
    # Validate the complete merge tree before any database or source-invoice
    # change. Identical same-name files are safe remnants of an interrupted
    # run; differing files are warned about and left untouched in the source.
    foreach ($item in $archiveItems) {
        Test-ArchiveMerge -Source $item.FullName -Destination (Join-Path $archivePath $item.Name)
    }

    $script:mysqlExe = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
    if (-not (Test-Path -LiteralPath $script:mysqlExe -PathType Leaf)) { throw "mysql.exe was not found: $script:mysqlExe" }

    $runtimeConfig = Join-Path $ApplicationRoot 'backend\printer_server\gstRuntimeConfig.js'
    $templatePath = Join-Path $ApplicationRoot 'runOnMarch31\structureOfChangableDB.sql'
    if (-not (Test-Path -LiteralPath $runtimeConfig -PathType Leaf)) { throw "Database configuration was not found: $runtimeConfig" }
    if (-not (Test-Path -LiteralPath $templatePath -PathType Leaf)) { throw "Database structure template was not found: $templatePath" }
    $configText = Get-Content -Raw -LiteralPath $runtimeConfig
    if ($configText -notmatch "(?m)^\s*password:\s*'([^']+)'\s*$") { throw 'Could not read the legacy database password contract.' }
    $databasePassword = $Matches[1]
    $env:MYSQL_PWD = $databasePassword

    $sourceExists = Invoke-MySql "SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name='$sourceDatabase';"
    if ($sourceExists -ne '1') { throw "Source database does not exist: $sourceDatabase" }

    $targetExists = Invoke-MySql "SELECT COUNT(*) FROM information_schema.schemata WHERE schema_name='$targetDatabase';"
    $rolloverAlreadyComplete = $false
    if ($targetExists -eq '1') {
        $markerExists = Invoke-MySql "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$targetDatabase' AND table_name='_hosangadi_rollover';"
        if ($markerExists -eq '1') {
            $rolloverAlreadyComplete = (Invoke-MySql "SELECT COUNT(*) FROM ``$targetDatabase``.``_hosangadi_rollover`` WHERE source_year=$sourceYear;") -eq '1'
        }
    }

    if (-not $rolloverAlreadyComplete) {
        $backupDirectory = 'C:\backup'
        New-Item -ItemType Directory -Path $backupDirectory -Force | Out-Null
        $fullBackupPath = Join-Path $backupDirectory "aFullBackup_$($now.ToString('yyyy-MM-dd')).sql"
        if (Test-Path -LiteralPath $fullBackupPath -PathType Leaf) {
            if ((Get-Item -LiteralPath $fullBackupPath).Length -eq 0) { throw "Existing pre-rollover backup is empty: $fullBackupPath" }
            Write-RolloverLog "FULL BACKUP REUSED $fullBackupPath"
        } else {
            $hasBackupMutex = $backupMutex.WaitOne(0)
            if (-not $hasBackupMutex) { throw 'Another Hosangadi database backup is running. Wait for it to finish and rerun the rollover.' }

            $mysqlDumpExe = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysqldump.exe'
            if (-not (Test-Path -LiteralPath $mysqlDumpExe -PathType Leaf)) { throw "mysqldump.exe was not found: $mysqlDumpExe" }
            $databaseOutput = Invoke-MySql "SELECT schema_name FROM information_schema.schemata WHERE schema_name='somanath' OR schema_name REGEXP '^somanath20[0-9]{2,4}$' ORDER BY schema_name;"
            $applicationDatabases = @($databaseOutput -split '\r?\n' | Where-Object { $_ -match '^somanath(?:20\d{2,4})?$' })
            if ($applicationDatabases -notcontains 'somanath' -or $applicationDatabases -notcontains $sourceDatabase) {
                throw "Full-backup database inventory is incomplete: $($applicationDatabases -join ', ')"
            }

            $temporaryBackupPath = "$fullBackupPath.partial"
            $backupErrorPath = "$temporaryBackupPath.error"
            Remove-Item -LiteralPath $temporaryBackupPath, $backupErrorPath -Force -ErrorAction SilentlyContinue
            $dumpArguments = @(
                '--host=localhost', '--port=3306', '--user=root',
                '--single-transaction', '--routines', '--triggers', '--events',
                '--set-gtid-purged=OFF', '--no-tablespaces', '--databases'
            ) + $applicationDatabases
            $dumpProcess = Start-Process -FilePath $mysqlDumpExe -ArgumentList $dumpArguments `
                -RedirectStandardOutput $temporaryBackupPath -RedirectStandardError $backupErrorPath `
                -WindowStyle Hidden -Wait -PassThru
            if ($dumpProcess.ExitCode -ne 0) {
                $details = if (Test-Path -LiteralPath $backupErrorPath) { (Get-Content -Raw -LiteralPath $backupErrorPath).Trim() } else { 'No mysqldump error text was produced.' }
                throw "Pre-rollover mysqldump failed with exit code $($dumpProcess.ExitCode): $details"
            }
            if (-not (Test-Path -LiteralPath $temporaryBackupPath) -or (Get-Item -LiteralPath $temporaryBackupPath).Length -eq 0) {
                throw 'Pre-rollover mysqldump produced an empty backup.'
            }
            Move-Item -LiteralPath $temporaryBackupPath -Destination $fullBackupPath
            Remove-Item -LiteralPath $backupErrorPath -Force -ErrorAction SilentlyContinue
            Write-RolloverLog "FULL BACKUP SUCCESS databases=$($applicationDatabases -join ',') path=$fullBackupPath"
            Write-Host "Full pre-rollover backup created: $fullBackupPath"

            $backupMutex.ReleaseMutex()
            $hasBackupMutex = $false
        }
    }

    if ($targetExists -eq '0') {
        $template = Get-Content -Raw -LiteralPath $templatePath
        $template = [regex]::Replace($template, '(?im)^CREATE DATABASE[^;]+;\s*', '', 1)
        $template = [regex]::Replace($template, '(?im)^USE\s+`[^`]+`;\s*', '', 1)
        Invoke-MySql "CREATE DATABASE IF NOT EXISTS ``$targetDatabase`` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci; USE ``$targetDatabase``; $template" | Out-Null
    }

    $requiredTables = 'acc_bal','cashflow_purchase','cashflow_sales','max_id','purchases','sales','sales_sp','stocks'
    $tableCount = Invoke-MySql "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$targetDatabase' AND table_name IN ('$($requiredTables -join "','")');"
    if ([int]$tableCount -ne $requiredTables.Count) { throw "$targetDatabase does not contain the complete expected table structure." }

    Invoke-MySql "CREATE TABLE IF NOT EXISTS ``$targetDatabase``.``_hosangadi_rollover`` (source_year int NOT NULL PRIMARY KEY, completed_at datetime NOT NULL, account_rows int NOT NULL, stock_rows int NOT NULL) ENGINE=InnoDB;" | Out-Null
    $completed = Invoke-MySql "SELECT COUNT(*) FROM ``$targetDatabase``.``_hosangadi_rollover`` WHERE source_year=$sourceYear;"
    if ($completed -ne '1') {
        $operationalRows = Invoke-MySql "SELECT (SELECT COUNT(*) FROM ``$targetDatabase``.purchases)+(SELECT COUNT(*) FROM ``$targetDatabase``.sales)+(SELECT COUNT(*) FROM ``$targetDatabase``.cashflow_purchase)+(SELECT COUNT(*) FROM ``$targetDatabase``.cashflow_sales);"
        if ([int64]$operationalRows -ne 0) { throw "$targetDatabase already contains transactions but has no completed rollover marker; manual review is required." }

        $carrySql = @"
START TRANSACTION;
DELETE FROM ``$targetDatabase``.acc_bal;
DELETE FROM ``$targetDatabase``.stocks;
DELETE FROM ``$targetDatabase``.max_id;
INSERT INTO ``$targetDatabase``.acc_bal
SELECT acc_id, acc_cls_bal_firm1, acc_cls_bal_firm2, acc_cls_bal_firm3,
       acc_cls_bal_firm1, acc_cls_bal_firm2, acc_cls_bal_firm3
FROM ``$sourceDatabase``.acc_bal;
INSERT INTO ``$targetDatabase``.stocks
(stk_id,stk_pur_id,stk_prod_id,stk_prod_qty,stk_tot_qty,stk_cost,stk_sp_nml,stk_sp_htl,stk_sp_spl,stk_sp_ang,stk_exp,stk_sup_id,stk_firm_id,insert_time,insert_id,update_time,update_id)
SELECT CONCAT('$targetShort','_',ROW_NUMBER() OVER (ORDER BY stk_id)), stk_pur_id,stk_prod_id,stk_prod_qty,stk_tot_qty,stk_cost,stk_sp_nml,stk_sp_htl,stk_sp_spl,stk_sp_ang,stk_exp,stk_sup_id,stk_firm_id,insert_time,insert_id,NULL,NULL
FROM ``$sourceDatabase``.stocks WHERE stk_prod_qty > 0;
INSERT INTO ``$targetDatabase``.max_id VALUES (0,0,(SELECT COUNT(*) FROM ``$targetDatabase``.stocks),0,0,0,0,0);
INSERT INTO ``$targetDatabase``.``_hosangadi_rollover``
VALUES ($sourceYear,NOW(),(SELECT COUNT(*) FROM ``$targetDatabase``.acc_bal),(SELECT COUNT(*) FROM ``$targetDatabase``.stocks));
COMMIT;
"@
        Invoke-MySql $carrySql | Out-Null
        Write-RolloverLog "DATABASE SUCCESS $sourceDatabase -> $targetDatabase"
    }

    foreach ($item in $archiveItems) {
        if (Test-Path -LiteralPath $item.FullName) {
            Merge-ArchiveItem -Source $item.FullName -Destination (Join-Path $archivePath $item.Name)
        }
    }

    Write-RolloverLog "COMPLETE $sourceDatabase -> $targetDatabase; invoices -> $archivePath"
    Write-Host "Financial-year rollover complete: $sourceDatabase -> $targetDatabase"
    Write-Host "Old invoices archived in: $archivePath"
} catch {
    Write-RolloverLog "ERROR $($_.Exception.Message) AT $($_.ScriptStackTrace)"
    Write-Error -ErrorRecord $_
    exit 1
} finally {
    $databasePassword = $null
    Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue
    if ($hasMutex) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
    if ($hasBackupMutex) { $backupMutex.ReleaseMutex() }
    $backupMutex.Dispose()
}
