# GST Monthly Automation

This workflow generates and emails the previous calendar month's GST files for `SOMANATH STORES`:

- `Exempted_MONTH.txt`
- `Purchase_MONTH.xlsx`
- `GSTR1_MONTH.xlsx`

It reuses the existing Purchase and Sales report endpoints in `backend/printer_server/printerServer.js`. Reports remain in the existing `%USERPROFILE%\angadiImages` directory; the automation does not create extra Desktop report copies.

## Runtime behavior

- Scheduled execution: first Saturday of every month at 10:00 AM.
- Reporting period: previous completed calendar month.
- Financial year: April through March (`somanath2026` for April 2026 through March 2027).
- Invoice range: first and last non-null `trans_sales` ordered by `cashflow_sales.insert_time` within the reporting month.
- Auditor subject: `GST Returns - SOMANATH STORES - Month YYYY`.
- Auditor recipient: `jathindra_co@yahoo.com`.
- CC: `vshivanand2@gmail.com`.
- Failure recipient: only `vshivanand2@gmail.com`.
- A no-data condition is treated as a failure and never sends an auditor email.

The workflow generates Purchase/Exempted first, waits for successful completion, then generates GSTR1. All three files must be fresh, nonempty, readable, and contain their expected workbook sheets before email delivery begins.

## Install dependencies

From Command Prompt or PowerShell:

```powershell
cd backend\printer_server
npm.cmd install
```

`npm.cmd` is used because some Windows PowerShell configurations block the `npm.ps1` wrapper.

## Configuration

The committed example is:

`backend\printer_server\gst-monthly-automation.env.example`

The default live configuration location is outside the repository:

`%LOCALAPPDATA%\Hosangadi\gst-monthly-automation\gst-monthly-automation.env`

The scheduler installer creates that file from the example when it does not exist. Edit it and set:

```text
GST_MONTHLY_AUTOMATION_ENABLED=true
GST_SMTP_PASSWORD=your_16_character_gmail_app_password
```

Do not add the real Gmail App Password to a committed repository file. The repository's existing local MySQL defaults are used unless `GST_DB_HOST`, `GST_DB_PORT`, `GST_DB_USER`, or `GST_DB_PASSWORD` is set in the live configuration.

### Enable or disable scheduled execution

Edit the live configuration file:

```text
GST_MONTHLY_AUTOMATION_ENABLED=false
```

The scheduled task remains installed but exits successfully without accessing MySQL, generating reports, or sending email. Change it back to `true` to re-enable it. Manual runs remain available in either state.

## Install the Windows scheduled task

Run PowerShell as the Windows user that operates Hosangadi:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_gst_monthly_task.ps1
```

The task is named `Hosangadi GST Monthly Automation`. It runs with that user's interactive token, preventing a hardcoded Windows username and keeping `%USERPROFILE%`, output, logs, and Desktop fallback paths consistent if the repository is moved to a replacement computer.

The task has `StartWhenAvailable` enabled. If the computer is off at 10:00 AM on the first Saturday, Windows Task Scheduler runs it when the task becomes available after the user next logs on.

To remove the scheduled task:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\install_gst_monthly_task.ps1 -Uninstall
```

After moving to a replacement computer, install Node.js and dependencies, copy the live configuration to the new user's `%LOCALAPPDATA%` location, and run the installer again from the new repository location. The action uses absolute paths generated at installation time, so reinstalling the task after a move is required.

## Manual execution

Windows Command Prompt (recommended on the inspected system):

```bat
run_gst_monthly_workflow.bat
```

PowerShell:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\run_gst_monthly_workflow.ps1
```

Git Bash, if installed later:

```bash
./run_gst_monthly_workflow.sh
```

All launchers call the same Node entry point and return its exit code. A normal manual run processes the previous month even when scheduled automation is disabled.

Retry a specific failed month:

```bat
run_gst_monthly_workflow.bat --month 2026-07
```

A failed month can be retried normally. A month recorded as successfully emailed is skipped. To intentionally resend a successful month—or resolve a run that stopped during SMTP delivery—review the sent mailbox first, then use:

```bat
run_gst_monthly_workflow.bat --month 2026-07 --force
```

Scheduled execution never accepts `--force`.

## Logs, state, and duplicate protection

Default runtime directory:

`%LOCALAPPDATA%\Hosangadi\gst-monthly-automation`

It contains:

- One log per reporting month.
- `state.json`, keyed by firm and reporting month.
- A temporary exclusive run lock.

The state transition before auditor delivery is `email_sending`, followed by `email_sent` only after SMTP confirms acceptance. If the process stops during that narrow interval, automatic runs do not resend; manual review and `--force` are required. Task Scheduler and the workflow lock also prevent overlapping instances.

## Failure handling

Any database, invoice-query, report-generation, verification, mail-construction, SMTP, or unexpected runtime failure:

1. Is logged locally with its workflow stage.
2. Is recorded as failed unless auditor delivery may already be in progress.
3. Sends a failure notification only to `vshivanand2@gmail.com`.
4. If that notification also fails, writes `GST_Automation_Error_YYYY-MM-DD_HH-MM-SS.txt` to the Windows known Desktop folder.

Credentials and environment values whose names indicate passwords, tokens, secrets, or authorization are redacted from logs and failure details.

## Testing

Run unit tests without contacting MySQL or SMTP:

```powershell
cd backend\printer_server
npm.cmd test
```

Check command-line setup without running the workflow:

```powershell
node gstMonthlyWorkflow.js --help
```

Before the first live run:

1. Confirm MySQL is reachable from the target system with the configured values.
2. Confirm the three backend services can start and the existing GST Returns screen can generate both reports.
3. Add the Gmail App Password to the live configuration.
4. Leave `GST_MONTHLY_AUTOMATION_ENABLED=false` and perform a controlled manual run for a known completed month.
5. Verify the three attachments, invoice range, recipient, CC, and sent email.
6. Set `GST_MONTHLY_AUTOMATION_ENABLED=true` only after that validation.

Manual execution sends a real auditor email. Use a temporary `GST_EMAIL_TO`/`GST_EMAIL_CC` override in the live configuration for a non-auditor acceptance test.
