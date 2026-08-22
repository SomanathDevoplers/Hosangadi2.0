[CmdletBinding()]
param(
    [string]$ApplicationRoot = (Split-Path $PSScriptRoot -Parent),
    [string]$InvoiceRoot = (Join-Path $env:USERPROFILE 'Desktop\Invoices'),
    [switch]$Force
)

#Requires -Version 5.1
$ErrorActionPreference = 'Stop'
Set-StrictMode -Version 2.0

$mutex = New-Object Threading.Mutex($false, 'Global\HosangadiFinancialYearRollover')
$hasMutex = $false
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

try {
    $hasMutex = $mutex.WaitOne(0)
    if (-not $hasMutex) { exit 0 }

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

    $oldInvoices = Join-Path $InvoiceRoot 'oldinvoices'
    $archivePath = Join-Path $oldInvoices $archiveName
    New-Item -ItemType Directory -Path $archivePath -Force | Out-Null
    $items = @(Get-ChildItem -LiteralPath $oldInvoices -Force | Where-Object { $_.Name -ne $archiveName })
    foreach ($item in $items) {
        $destination = Join-Path $archivePath $item.Name
        if (Test-Path -LiteralPath $destination) { throw "Invoice archive collision: $destination" }
        Move-Item -LiteralPath $item.FullName -Destination $archivePath
    }

    Write-RolloverLog "COMPLETE $sourceDatabase -> $targetDatabase; invoices -> $archivePath"
    Write-Host "Financial-year rollover complete: $sourceDatabase -> $targetDatabase"
    Write-Host "Old invoices archived in: $archivePath"
} catch {
    Write-RolloverLog "ERROR $($_.Exception.Message)"
    Write-Error $_
    exit 1
} finally {
    $databasePassword = $null
    Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue
    if ($hasMutex) { $mutex.ReleaseMutex() }
    $mutex.Dispose()
}
