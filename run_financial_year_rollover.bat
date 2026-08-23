@echo off
setlocal
cd /d "%~dp0"
powershell.exe -NoProfile -ExecutionPolicy Bypass -File "%~dp0scripts\invoke_financial_year_rollover.ps1" -ApplicationRoot "%~dp0."
if errorlevel 1 (
  echo.
  echo Financial-year rollover FAILED. Review C:\ProgramData\Hosangadi\financial-year-rollover.log
) else (
  echo.
  echo Financial-year rollover completed successfully.
)
pause
endlocal
