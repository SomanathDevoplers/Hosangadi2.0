#Requires -Version 5.1
#Requires -RunAsAdministrator

[CmdletBinding()]
param(
    [string]$DatabaseBackupPath,
    [string]$PrebuiltLoginDirectory,
    [string]$PrebuiltRootDirectory,
    [string]$MySqlInstallerPath,
    [switch]$InstallPrerequisites,
    [switch]$SkipDatabaseRestore,
    [switch]$SkipFrontendBuild,
    [switch]$SkipNodeInstall,
    [switch]$SkipDatabaseBackupTask,
    [switch]$SkipDatabaseBackupCleanupTask,
    [switch]$NoShutdownBackupTrigger,
    [switch]$EnableGstAutomation
)

$ErrorActionPreference = 'Stop'
$ProgressPreference = 'SilentlyContinue'
Set-StrictMode -Version 2.0

$Expected = @{
    Python = '3.14.3'
    Node = '22.22.2'
    Npm = '10.9.7'
    MySqlMinimum = '8.0.45'
    Pm2 = '6.0.14'
    Pm2Startup = '1.0.3'
    AutoPyToExe = '2.50.0'
    PyInstaller = '6.19.0'
}

$RepositoryRoot = Split-Path $PSScriptRoot -Parent
$FrontendSource = Join-Path $RepositoryRoot 'frontend'
$BackendSource = Join-Path $RepositoryRoot 'backend'
$ProgramDirectory = Join-Path $env:ProgramFiles 'Hosangadi2.0'
$DeploymentRoot = Join-Path $env:USERPROFILE 'Hosangadi2.0'
$BackendDestination = Join-Path $DeploymentRoot 'backend'
$InvoiceDirectory = Join-Path $env:USERPROFILE 'Desktop\Invoices'
$ImageStagingDirectory = Join-Path $env:USERPROFILE 'Images'
$ImageStoreDirectory = Join-Path $env:USERPROFILE 'angadiImages'
$BackupDirectory = 'C:\backup'
$SetupTemp = Join-Path $env:TEMP 'Hosangadi-setup'
$LogPath = Join-Path $env:TEMP ("Hosangadi-setup-{0}.log" -f (Get-Date -Format 'yyyyMMdd-HHmmss'))
$GhostscriptInstallerHash = '9C7BBC5DAA9F5869D48DD1480F6D758E181FD4FAD2822B51CBBF568C91C39E0A'
$GhostscriptMarkerDirectory = Join-Path $env:ProgramData 'Hosangadi'
$GhostscriptMarker = Join-Path $GhostscriptMarkerDirectory 'ghostscript-installer.sha256'

function Write-Step([string]$Message) {
    Write-Host "`n=== $Message ===" -ForegroundColor Cyan
}

function Invoke-Checked {
    param([Parameter(Mandatory)][string]$FilePath, [string[]]$ArgumentList, [string]$WorkingDirectory)
    if ($WorkingDirectory) { Push-Location $WorkingDirectory }
    try {
        & $FilePath @ArgumentList
        if ($LASTEXITCODE -ne 0) { throw "$FilePath failed with exit code $LASTEXITCODE" }
    } finally {
        if ($WorkingDirectory) { Pop-Location }
    }
}

function Refresh-ProcessPath {
    $machine = [Environment]::GetEnvironmentVariable('Path', 'Machine')
    $user = [Environment]::GetEnvironmentVariable('Path', 'User')
    $env:Path = "$machine;$user"
}

function Get-CommandVersion([string]$Command, [string[]]$Arguments) {
    $resolved = Get-Command $Command -ErrorAction SilentlyContinue
    if (-not $resolved) { return $null }
    $text = (& $resolved.Source @Arguments 2>&1 | Out-String).Trim()
    if ($text -match '(\d+\.\d+\.\d+)') { return $Matches[1] }
    return $null
}

function Assert-Version([string]$Name, [string]$Actual, [string]$Wanted, [string]$Instruction) {
    if (-not $Actual) { throw "$Name was not found. $Instruction" }
    if ($Actual -ne $Wanted) { throw "$Name $Actual is active, but $Wanted is required. $Instruction" }
    Write-Host "OK: $Name $Actual"
}

function Install-DownloadedPackage {
    param(
        [Parameter(Mandatory)][string]$Name,
        [Parameter(Mandatory)][uri]$Uri,
        [Parameter(Mandatory)][string]$FileName,
        [Parameter(Mandatory)][string[]]$Arguments
    )
    New-Item -ItemType Directory -Path $SetupTemp -Force | Out-Null
    $destination = Join-Path $SetupTemp $FileName
    if (-not (Test-Path -LiteralPath $destination)) {
        Write-Host "Downloading $Name from $Uri"
        Invoke-WebRequest -Uri $Uri -OutFile $destination -UseBasicParsing
    }
    $signature = Get-AuthenticodeSignature -LiteralPath $destination
    if ($signature.Status -ne 'Valid') { throw "$Name installer signature is not valid: $($signature.Status)" }
    $process = Start-Process -FilePath $destination -ArgumentList $Arguments -Wait -PassThru
    if ($process.ExitCode -notin 0, 1641, 3010) { throw "$Name installer exited with $($process.ExitCode)" }
    Refresh-ProcessPath
}

function Ensure-Directory([string]$Path) {
    if (-not (Test-Path -LiteralPath $Path -PathType Container)) {
        New-Item -ItemType Directory -Path $Path -Force | Out-Null
        Write-Host "Created $Path"
    }
}

function Grant-CurrentUserModify([string]$Path) {
    $identity = [Security.Principal.WindowsIdentity]::GetCurrent().Name
    Invoke-Checked -FilePath 'icacls.exe' -ArgumentList @($Path, '/grant', "$identity`:(OI)(CI)M", '/T', '/C', '/Q')
}

function Copy-TreePreservingRuntimeFiles([string]$Source, [string]$Destination) {
    Ensure-Directory $Destination
    & robocopy.exe $Source $Destination /E /R:2 /W:2 /XD node_modules /XF .env NodeErr.txt /NFL /NDL /NJH /NJS /NP
    if ($LASTEXITCODE -gt 7) { throw "robocopy failed with exit code $LASTEXITCODE" }
}

function Convert-SecureStringToPlainText([Security.SecureString]$SecureValue) {
    $pointer = [Runtime.InteropServices.Marshal]::SecureStringToBSTR($SecureValue)
    try { return [Runtime.InteropServices.Marshal]::PtrToStringBSTR($pointer) }
    finally { [Runtime.InteropServices.Marshal]::ZeroFreeBSTR($pointer) }
}

Start-Transcript -Path $LogPath | Out-Null
try {
    Write-Step 'Repository preflight'
    foreach ($required in @(
        (Join-Path $FrontendSource 'login.py'),
        (Join-Path $FrontendSource 'root.py'),
        (Join-Path $FrontendSource 'requirements.txt'),
        (Join-Path $BackendSource 'ecosystem.config.js'),
        (Join-Path $RepositoryRoot 'ghostScript.exe')
    )) {
        if (-not (Test-Path -LiteralPath $required)) { throw "Required repository file is missing: $required" }
    }
    Write-Host "Repository: $RepositoryRoot"
    Write-Host "Installing for Windows user: $env:USERDOMAIN\$env:USERNAME"

    Write-Step 'Python and Node prerequisites'
    # An elevated terminal opened before a prerequisite was installed retains
    # its old process PATH, and child powershell.exe processes inherit it.
    # Reload persisted machine/user values before discovering executables.
    Refresh-ProcessPath
    $pythonVersion = Get-CommandVersion 'python.exe' @('--version')
    if (-not $pythonVersion -and $InstallPrerequisites) {
        Install-DownloadedPackage -Name 'Python 3.14.3' `
            -Uri 'https://www.python.org/ftp/python/3.14.3/python-3.14.3-amd64.exe' `
            -FileName 'python-3.14.3-amd64.exe' `
            -Arguments @('/quiet', 'InstallAllUsers=1', 'PrependPath=1', 'Include_launcher=1', 'Include_test=0')
        $pythonVersion = Get-CommandVersion 'python.exe' @('--version')
    }
    Assert-Version 'Python' $pythonVersion $Expected.Python 'Install Python 3.14.3 x64, or rerun with -InstallPrerequisites.'

    $nodeVersion = Get-CommandVersion 'node.exe' @('--version')
    if (-not $nodeVersion -and $InstallPrerequisites) {
        Install-DownloadedPackage -Name 'Node.js 22.22.2' `
            -Uri 'https://nodejs.org/dist/v22.22.2/node-v22.22.2-x64.msi' `
            -FileName 'node-v22.22.2-x64.msi' `
            -Arguments @('/qn', '/norestart')
        $nodeVersion = Get-CommandVersion 'node.exe' @('--version')
    }
    Assert-Version 'Node.js' $nodeVersion $Expected.Node 'Install Node.js 22.22.2 x64, or rerun with -InstallPrerequisites.'
    Assert-Version 'npm' (Get-CommandVersion 'npm.cmd' @('--version')) $Expected.Npm 'Use the npm bundled with the confirmed Node.js installation.'

    Write-Step 'Ghostscript'
    $gsInstaller = Join-Path $RepositoryRoot 'ghostScript.exe'
    $actualGsHash = (Get-FileHash -Algorithm SHA256 -LiteralPath $gsInstaller).Hash
    if ($actualGsHash -ne $GhostscriptInstallerHash) { throw 'Bundled Ghostscript installer hash does not match the audited repository artifact.' }
    $signature = Get-AuthenticodeSignature -LiteralPath $gsInstaller
    if ($signature.Status -ne 'Valid' -or $signature.SignerCertificate.Subject -notmatch 'Artifex Software') {
        throw "Bundled Ghostscript signature validation failed: $($signature.Status)"
    }
    $ghostscript = Get-ChildItem (Join-Path $env:ProgramFiles 'gs\gs*\bin\gswin64c.exe') -ErrorAction SilentlyContinue |
        Sort-Object FullName -Descending | Select-Object -First 1
    $markerHash = if (Test-Path -LiteralPath $GhostscriptMarker) { (Get-Content -Raw -LiteralPath $GhostscriptMarker).Trim() } else { $null }
    if (-not $ghostscript -or $markerHash -ne $GhostscriptInstallerHash) {
        $process = Start-Process -FilePath $gsInstaller -ArgumentList '/S' -Wait -PassThru
        if ($process.ExitCode -ne 0) { throw "Ghostscript installer exited with $($process.ExitCode)" }
        $ghostscript = Get-ChildItem (Join-Path $env:ProgramFiles 'gs\gs*\bin\gswin64c.exe') -ErrorAction SilentlyContinue |
            Sort-Object FullName -Descending | Select-Object -First 1
        Ensure-Directory $GhostscriptMarkerDirectory
        Set-Content -LiteralPath $GhostscriptMarker -Value $GhostscriptInstallerHash -Encoding ASCII
    }
    if (-not $ghostscript) { throw 'Ghostscript executable was not found after installation.' }
    Write-Host "OK: Ghostscript $($ghostscript.FullName)"

    Write-Step 'Required directories and ACLs'
    $directories = @(
        $ProgramDirectory, $BackupDirectory, $DeploymentRoot, $BackendDestination,
        $InvoiceDirectory, (Join-Path $InvoiceDirectory 'barcode'),
        (Join-Path $InvoiceDirectory 'oldinvoices'), (Join-Path $InvoiceDirectory 'oldinvoices\voucher'),
        (Join-Path $InvoiceDirectory 'reports'), $ImageStagingDirectory,
        (Join-Path $ImageStagingDirectory 'firms'), (Join-Path $ImageStagingDirectory 'categories'),
        (Join-Path $ImageStagingDirectory 'accounts'), (Join-Path $ImageStagingDirectory 'products'),
        $ImageStoreDirectory, (Join-Path $ImageStoreDirectory 'firms'),
        (Join-Path $ImageStoreDirectory 'categories'), (Join-Path $ImageStoreDirectory 'employs'),
        (Join-Path $ImageStoreDirectory 'accounts'), (Join-Path $ImageStoreDirectory 'products'),
        (Join-Path $env:LOCALAPPDATA 'Hosangadi\gst-monthly-automation')
    )
    $directories | ForEach-Object { Ensure-Directory $_ }
    Grant-CurrentUserModify $ProgramDirectory
    Grant-CurrentUserModify $BackupDirectory

    Write-Step 'Application files'
    $resolvedBackendSource = (Resolve-Path -LiteralPath $BackendSource).Path.TrimEnd('\')
    $resolvedBackendDestination = (Resolve-Path -LiteralPath $BackendDestination).Path.TrimEnd('\')
    if ($resolvedBackendSource -ine $resolvedBackendDestination) {
        Copy-TreePreservingRuntimeFiles $BackendSource $BackendDestination
    } else {
        Write-Host 'Repository backend is already at the required deployment path; copy skipped.'
    }
    $nodeErr = Join-Path $BackendDestination 'socket_server\NodeErr.txt'
    if (-not (Test-Path -LiteralPath $nodeErr)) {
        Copy-Item -LiteralPath (Join-Path $BackendSource 'socket_server\NodeErr.txt') -Destination $nodeErr
    }
    Copy-Item -Path (Join-Path $FrontendSource 'files\*') -Destination $ProgramDirectory -Force

    Write-Step 'Python environment and frontend builds'
    Invoke-Checked -FilePath 'python.exe' -ArgumentList @('-m', 'pip', 'install', '--disable-pip-version-check', '-r', (Join-Path $FrontendSource 'requirements.txt'))
    # Avoid an embedded quoted string here: Windows PowerShell 5.1 can strip
    # those quotes while forwarding a native executable's -c argument.
    Invoke-Checked -FilePath 'python.exe' -ArgumentList @('-c', 'import requests, PIL, reportlab, playsound, socketio, pyperclip, tkdocviewer; print(True)')
    Assert-Version 'auto-py-to-exe' (Get-CommandVersion 'python.exe' @('-m', 'pip', 'show', 'auto-py-to-exe')) $Expected.AutoPyToExe 'Reinstall frontend/requirements.txt.'
    # Invoking `python -m PyInstaller --version` as administrator writes a
    # deprecation notice to stderr. Under this script's strict error handling,
    # that harmless notice can look like a failed version check. Read the
    # installed module version without starting PyInstaller instead.
    Assert-Version 'PyInstaller' (Get-CommandVersion 'python.exe' @('-c', 'import PyInstaller; print(PyInstaller.__version__)')) $Expected.PyInstaller 'Reinstall frontend/requirements.txt.'

    $loginDestination = Join-Path $ProgramDirectory 'login'
    $rootDestination = Join-Path $ProgramDirectory 'root'
    if ($PrebuiltLoginDirectory -or $PrebuiltRootDirectory) {
        if (-not ($PrebuiltLoginDirectory -and $PrebuiltRootDirectory)) { throw 'Provide both prebuilt directories or neither.' }
        if (-not (Test-Path (Join-Path $PrebuiltLoginDirectory 'login.exe'))) { throw 'Prebuilt login.exe was not found.' }
        if (-not (Test-Path (Join-Path $PrebuiltRootDirectory 'root.exe'))) { throw 'Prebuilt root.exe was not found.' }
        Ensure-Directory $loginDestination; Ensure-Directory $rootDestination
        Copy-Item -Path (Join-Path $PrebuiltLoginDirectory '*') -Destination $loginDestination -Recurse -Force
        Copy-Item -Path (Join-Path $PrebuiltRootDirectory '*') -Destination $rootDestination -Recurse -Force
    } elseif (-not $SkipFrontendBuild) {
        $buildRoot = Join-Path $RepositoryRoot '.setup-build'
        $distRoot = Join-Path $buildRoot 'dist'
        if (Test-Path -LiteralPath $buildRoot) { Remove-Item -LiteralPath $buildRoot -Recurse -Force }
        Ensure-Directory $buildRoot
        foreach ($entry in @('login', 'root')) {
            Invoke-Checked -FilePath 'python.exe' -WorkingDirectory $FrontendSource -ArgumentList @(
                '-m', 'PyInstaller', '--noconfirm', '--clean', '--onedir', '--windowed',
                '--name', $entry, '--icon', (Join-Path $FrontendSource 'files\logo_hosagadi.ico'),
                '--distpath', $distRoot, '--workpath', (Join-Path $buildRoot "work-$entry"),
                '--specpath', $buildRoot, (Join-Path $FrontendSource "$entry.py")
            )
        }
        Ensure-Directory $loginDestination; Ensure-Directory $rootDestination
        Copy-Item -Path (Join-Path $distRoot 'login\*') -Destination $loginDestination -Recurse -Force
        Copy-Item -Path (Join-Path $distRoot 'root\*') -Destination $rootDestination -Recurse -Force
    }
    foreach ($exe in @((Join-Path $loginDestination 'login.exe'), (Join-Path $rootDestination 'root.exe'))) {
        if (-not (Test-Path -LiteralPath $exe)) { throw "Frontend executable is missing: $exe" }
    }

    Write-Step 'Desktop shortcut'
    $desktopDirectory = [Environment]::GetFolderPath('Desktop')
    if ([string]::IsNullOrWhiteSpace($desktopDirectory)) {
        $desktopDirectory = Join-Path $env:USERPROFILE 'Desktop'
    }
    Ensure-Directory $desktopDirectory
    $loginExecutable = Join-Path $loginDestination 'login.exe'
    $shortcutPath = Join-Path $desktopDirectory 'Hosangadi 2.0.lnk'
    $shell = New-Object -ComObject 'WScript.Shell'
    $shortcut = $shell.CreateShortcut($shortcutPath)
    $shortcut.TargetPath = $loginExecutable
    $shortcut.WorkingDirectory = $loginDestination
    $shortcut.IconLocation = "$loginExecutable,0"
    $shortcut.Description = 'Launch Hosangadi 2.0'
    $shortcut.Save()
    Write-Host "OK: Desktop shortcut: $shortcutPath"

    Write-Step 'Node dependencies and PM2'
    foreach ($service in @('socket_server', 'product_server', 'report_server', 'printer_server', 'barcode_server')) {
        $serviceDirectory = Join-Path $BackendDestination $service
        if ($SkipNodeInstall) {
            if (-not (Test-Path -LiteralPath (Join-Path $serviceDirectory 'node_modules') -PathType Container)) {
                throw "-SkipNodeInstall was supplied, but deployed dependencies are missing for $service. Rerun without -SkipNodeInstall."
            }
            Write-Host "Reusing deployed Node dependencies: $service"
        } elseif (Test-Path (Join-Path $serviceDirectory 'package-lock.json')) {
            # Lifecycle scripts are required, notably for the Chromium used by html-pdf-node/Puppeteer.
            Invoke-Checked -FilePath 'npm.cmd' -WorkingDirectory $serviceDirectory -ArgumentList @('ci')
        } else {
            throw "A lockfile is missing for $service; refusing a non-reproducible npm install."
        }
    }
    if ($SkipNodeInstall) {
        Write-Host 'Reusing installed global PM2 packages.'
    } else {
        Invoke-Checked -FilePath 'npm.cmd' -ArgumentList @('install', '--global', "pm2@$($Expected.Pm2)", "pm2-windows-startup@$($Expected.Pm2Startup)")
    }
    Refresh-ProcessPath
    Assert-Version 'PM2' (Get-CommandVersion 'pm2.cmd' @('--version')) $Expected.Pm2 'Check the global npm binary directory in PATH.'
    $startupListing = (& npm.cmd list --global pm2-windows-startup --depth=0 2>&1 | Out-String)
    if ($startupListing -notmatch "pm2-windows-startup@$([regex]::Escape($Expected.Pm2Startup))") { throw 'pm2-windows-startup version verification failed.' }
    Invoke-Checked -FilePath 'pm2-startup.cmd' -ArgumentList @('install')

    Write-Step 'MySQL 8.0.45 and database restore'
    $mysqlCommand = Get-Command mysql.exe -ErrorAction SilentlyContinue
    $mysqlPath = if ($mysqlCommand) { $mysqlCommand.Source } else { $null }
    if (-not $mysqlPath) {
        $standardMysql = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
        if (Test-Path -LiteralPath $standardMysql) { $mysqlPath = $standardMysql }
    }
    if (-not $mysqlPath -and $MySqlInstallerPath) {
        if (-not (Test-Path -LiteralPath $MySqlInstallerPath)) { throw "MySQL installer not found: $MySqlInstallerPath" }
        Write-Host 'The MySQL installer will open. Install MySQL Server 8.0.45 and command-line tools to the standard path.'
        Start-Process -FilePath $MySqlInstallerPath -Wait
        Refresh-ProcessPath
        $standardMysql = 'C:\Program Files\MySQL\MySQL Server 8.0\bin\mysql.exe'
        $mysqlCommand = Get-Command mysql.exe -ErrorAction SilentlyContinue
        $mysqlPath = if ($mysqlCommand) { $mysqlCommand.Source } elseif (Test-Path -LiteralPath $standardMysql) { $standardMysql } else { $null }
    }
    if (-not $mysqlPath) { throw 'MySQL was not found. Install MySQL Server 8.0.45, or provide -MySqlInstallerPath.' }
    $mysqlPath = (Resolve-Path -LiteralPath $mysqlPath).Path
    $mysqlVersionText = (& $mysqlPath --version | Out-String)
    $mysqlVersionMatch = [regex]::Match($mysqlVersionText, '\b(\d+\.\d+\.\d+)\b')
    if (-not $mysqlVersionMatch.Success) { throw "Could not determine the MySQL version from: $mysqlVersionText" }
    $mysqlVersion = [version]$mysqlVersionMatch.Groups[1].Value
    $minimumMySqlVersion = [version]$Expected.MySqlMinimum
    if ($mysqlVersion.Major -ne 8 -or $mysqlVersion.Minor -ne 0 -or $mysqlVersion -lt $minimumMySqlVersion) {
        throw "MySQL $($Expected.MySqlMinimum) or newer within the compatible 8.0.x series is required; found $mysqlVersion. MySQL 8.4+ is not accepted because the legacy application requires mysql_native_password."
    }
    Write-Host "OK: $($mysqlVersionText.Trim())"

    $legacyConfigText = Get-Content -Raw -LiteralPath (Join-Path $BackendDestination 'printer_server\gstRuntimeConfig.js')
    $passwordMatch = [regex]::Match($legacyConfigText, "(?m)^\s*password:\s*'([^']+)'\s*$")
    if (-not $passwordMatch.Success) { throw 'Could not read the legacy database password contract from gstRuntimeConfig.js.' }
    $plainPassword = $passwordMatch.Groups[1].Value
    $env:MYSQL_PWD = $plainPassword
    try {
        Invoke-Checked -FilePath $mysqlPath -ArgumentList @('--host=localhost', '--port=3306', '--user=root', '--execute', 'SELECT 1;')
        $plugin = (& $mysqlPath --host=localhost --port=3306 --user=root --batch --skip-column-names --execute="SELECT plugin FROM mysql.user WHERE user='root' AND host='localhost';" | Out-String).Trim()
        if ($LASTEXITCODE -ne 0) { throw 'Could not inspect the MySQL root authentication plugin.' }
        if ($plugin -ne 'mysql_native_password') {
            $escapedPassword = $plainPassword.Replace("'", "''")
            "ALTER USER 'root'@'localhost' IDENTIFIED WITH mysql_native_password BY '$escapedPassword';" |
                & $mysqlPath --host=localhost --port=3306 --user=root
            if ($LASTEXITCODE -ne 0) { throw 'Could not configure mysql_native_password for the legacy Node MySQL client.' }
            $escapedPassword = $null
        }

      if (-not $SkipDatabaseRestore) {
        if (-not $DatabaseBackupPath) { $DatabaseBackupPath = Read-Host 'Full path to the daily SQL backup containing master + current FY databases' }
        $DatabaseBackupPath = (Resolve-Path -LiteralPath $DatabaseBackupPath).Path
        # mysqldump writes CREATE DATABASE with a versioned comment such as
        # /*!32312 IF NOT EXISTS*/, so USE statements are the stable schema
        # boundary for dumps created with --databases.
        $schemas = @(
            Select-String -LiteralPath $DatabaseBackupPath -Pattern '(?i)^\s*USE\s+`?([a-z0-9_]+)`?\s*;' -AllMatches |
                ForEach-Object { $_.Matches } |
                ForEach-Object { $_.Groups[1].Value.ToLowerInvariant() } |
                Sort-Object -Unique
        )
        if ($schemas.Count -ne 2 -or $schemas -notcontains 'somanath' -or -not ($schemas | Where-Object { $_ -match '^somanath20\d{2,4}$' })) {
            throw "Backup must contain exactly master 'somanath' and one financial-year schema. Found: $($schemas -join ', ')"
        }
        Write-Host "Backup schemas validated: $($schemas -join ', ')"
        Ensure-Directory $SetupTemp
        $restoreCopy = Join-Path $SetupTemp 'database-restore.sql'
        Copy-Item -LiteralPath $DatabaseBackupPath -Destination $restoreCopy -Force
        $sourcePath = $restoreCopy.Replace('\', '/')
        Invoke-Checked -FilePath $mysqlPath -ArgumentList @('--host=localhost', '--port=3306', '--user=root', '--execute', "source $sourcePath")
        foreach ($schema in $schemas) {
            Invoke-Checked -FilePath $mysqlPath -ArgumentList @('--host=localhost', '--port=3306', '--user=root', '--batch', '--skip-column-names', '--execute', "SELECT COUNT(*) FROM information_schema.tables WHERE table_schema='$schema';")
        }
      }
    } finally {
        $plainPassword = $null
        Remove-Item Env:MYSQL_PWD -ErrorAction SilentlyContinue
    }

    if (-not $SkipDatabaseBackupTask) {
        Write-Step 'Scheduled database backups'
        $deployedScripts = Join-Path $DeploymentRoot 'scripts'
        Ensure-Directory $deployedScripts
        foreach ($scriptName in @(
            'backup_databases.ps1',
            'install_database_backup_task.ps1',
            'cleanup_database_backups.ps1',
            'install_database_backup_cleanup_task.ps1'
        )) {
            $sourceScript = Join-Path $RepositoryRoot "scripts\$scriptName"
            $destinationScript = Join-Path $deployedScripts $scriptName
            if ((Resolve-Path -LiteralPath $sourceScript).Path -ine $destinationScript) {
                Copy-Item -LiteralPath $sourceScript -Destination $destinationScript -Force
            }
        }
        $taskArguments = @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-File', (Join-Path $deployedScripts 'install_database_backup_task.ps1'),
            '-ApplicationRoot', $DeploymentRoot,
            '-BackupDirectory', $BackupDirectory
        )
        if ($NoShutdownBackupTrigger) { $taskArguments += '-NoShutdownTrigger' }
        Invoke-Checked -FilePath 'powershell.exe' -ArgumentList $taskArguments
    }

    if (-not $SkipDatabaseBackupCleanupTask) {
        Write-Step 'Weekly database-backup cleanup'
        $deployedScripts = Join-Path $DeploymentRoot 'scripts'
        Ensure-Directory $deployedScripts
        foreach ($scriptName in @('cleanup_database_backups.ps1', 'install_database_backup_cleanup_task.ps1')) {
            $sourceScript = Join-Path $RepositoryRoot "scripts\$scriptName"
            $destinationScript = Join-Path $deployedScripts $scriptName
            if ((Resolve-Path -LiteralPath $sourceScript).Path -ine $destinationScript) {
                Copy-Item -LiteralPath $sourceScript -Destination $destinationScript -Force
            }
        }
        Invoke-Checked -FilePath 'powershell.exe' -ArgumentList @(
            '-NoProfile', '-ExecutionPolicy', 'Bypass',
            '-File', (Join-Path $deployedScripts 'install_database_backup_cleanup_task.ps1'),
            '-ApplicationRoot', $DeploymentRoot,
            '-BackupDirectory', $BackupDirectory,
            '-RetentionDays', '6'
        )
    }

    Write-Step 'Starting backend services'
    Invoke-Checked -FilePath 'pm2.cmd' -ArgumentList @('startOrReload', (Join-Path $BackendDestination 'ecosystem.config.js'), '--update-env')
    Invoke-Checked -FilePath 'pm2.cmd' -ArgumentList @('save')

    Write-Step 'Printers'
    $printerNames = @(Get-Printer -ErrorAction SilentlyContinue | Select-Object -ExpandProperty Name)
    foreach ($requiredPrinter in @('BarcodePrinter', 'POS58 Printer')) {
        if ($printerNames -notcontains $requiredPrinter) { Write-Warning "Required Windows printer queue is missing: $requiredPrinter" }
    }
    if (-not (Get-CimInstance Win32_Printer -ErrorAction SilentlyContinue | Where-Object Default)) { Write-Warning 'No default Windows invoice printer is configured.' }

    if ($EnableGstAutomation) {
        Write-Step 'GST monthly scheduled task'
        $taskInstaller = Join-Path $DeploymentRoot 'scripts\install_gst_monthly_task.ps1'
        $deployedScripts = Join-Path $DeploymentRoot 'scripts'
        Ensure-Directory $deployedScripts
        Copy-Item -LiteralPath (Join-Path $RepositoryRoot 'scripts\install_gst_monthly_task.ps1') -Destination $taskInstaller -Force
        & powershell.exe -NoProfile -ExecutionPolicy Bypass -File $taskInstaller
        if ($LASTEXITCODE -ne 0) { throw 'GST scheduled-task installation failed.' }
        Write-Warning 'Edit backend\printer_server\.env, add the SMTP App Password, verify recipients, then enable the automation flag.'
    }

    Write-Step 'Final verification'
    Start-Sleep -Seconds 5
    $missingPorts = @()
    foreach ($port in @(4000, 5000, 6000, 7000, 8000)) {
        $listening = Get-NetTCPConnection -State Listen -LocalPort $port -ErrorAction SilentlyContinue
        if (-not $listening) { $missingPorts += $port }
        else { Write-Host "OK: TCP $port listening" }
    }
    if ($missingPorts.Count) { throw "Backend verification failed; ports not listening: $($missingPorts -join ', '). Run pm2 logs." }
    Write-Host "Setup completed. Transcript: $LogPath" -ForegroundColor Green
    Write-Host 'Manual checks still required: printers/default queue, SYSTEM-mode login, invoice/report generation, backup, and optional GST email.'
} catch {
    Write-Error $_
    Write-Host "Setup stopped safely. Fix the reported item and rerun the same command. Transcript: $LogPath" -ForegroundColor Yellow
    exit 1
} finally {
    Stop-Transcript -ErrorAction SilentlyContinue | Out-Null
}
