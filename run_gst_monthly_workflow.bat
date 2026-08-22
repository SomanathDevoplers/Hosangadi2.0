@echo off
setlocal

set "WORKFLOW=%~dp0backend\printer_server\gstMonthlyWorkflow.js"
where node.exe >nul 2>nul
if errorlevel 1 (
    echo FAILED: Node.js is not available on PATH. 1>&2
    exit /b 127
)

echo Starting the GST monthly workflow...
node.exe "%WORKFLOW%" --manual %*
set "WORKFLOW_EXIT=%ERRORLEVEL%"

if "%WORKFLOW_EXIT%"=="0" (
    echo GST monthly workflow finished successfully.
) else (
    echo GST monthly workflow failed with exit code %WORKFLOW_EXIT%. 1>&2
)

exit /b %WORKFLOW_EXIT%
