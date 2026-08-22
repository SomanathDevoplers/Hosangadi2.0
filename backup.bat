@echo off
setlocal

rem Financial year starts on April 1.
rem Jan-Mar use the previous calendar year; Apr-Dec use the current year.
for /f %%A in ('powershell.exe -NoProfile -Command "$d = Get-Date; if ($d.Month -lt 4) { $d.Year - 1 } else { $d.Year }"') do set "FY_START=%%A"
for /f %%A in ('powershell.exe -NoProfile -Command "Get-Date -Format yyyy-MM-dd"') do set "BACKUP_DATE=%%A"

set "FILENAME=somanathstores_%BACKUP_DATE%.sql"
set "YEAR_DATABASE=somanath%FY_START%"

if not exist "C:\backup" mkdir "C:\backup"

echo Backing up somanath and %YEAR_DATABASE%...
mysqldump -uroot -pmysqlpassword5 -h localhost --databases somanath %YEAR_DATABASE% > "C:\backup\%FILENAME%"
if errorlevel 1 (
    echo ERROR: MySQL backup failed.
    exit /b 1
)

if exist "D:\" (
    if not exist "D:\backup\" mkdir "D:\backup"
    xcopy /Q /Y /F "C:\backup\%FILENAME%" "D:\backup\"
) else (
    echo WARNING: D: drive is unavailable. The backup remains in C:\backup.
)

echo ...................................BACKUP AITHU..........................................
timeout /t 5
endlocal
