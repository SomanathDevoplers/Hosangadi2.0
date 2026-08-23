@echo off
setlocal
cd /d "%~dp0"

net session >nul 2>&1
if errorlevel 1 (
  echo Requesting Administrator permission...
  powershell.exe -NoProfile -ExecutionPolicy Bypass -Command "Start-Process -FilePath '%~f0' -Verb RunAs"
  exit /b
)

powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\restore_backup_system.ps1" -BackupFolder "%~dp0."
set "RESTORE_EXIT=%ERRORLEVEL%"

echo.
if "%RESTORE_EXIT%"=="0" (
  echo Backup-system database restoration completed successfully.
) else (
  echo Backup-system database restoration FAILED.
  echo Read the error above. No failed validation performs any database deletion.
)
echo.
pause
exit /b %RESTORE_EXIT%
