# Restore databases from a pendrive

Use this procedure when the standby computer must replace the failed main computer.

1. Connect the pendrive containing the latest completed `.sql` backup.
2. Confirm the backup filename, date and size. Do not select a `.partial` file.
3. Close Hosangadi and open 64-bit PowerShell as Administrator.
4. Change directory to the cloned Hosangadi repository.
5. Run the following command, replacing the example with the complete path to the selected backup:

```powershell
powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\scripts\setup_hosangadi.ps1 `
    -DatabaseBackupPath 'E:\backup\somanathstores_2026-08-22_14-00-03.sql'
```

Replace `E:` with the pendrive's actual drive letter. Keep single quotes around the path, especially when a directory name contains spaces.

The `-ExecutionPolicy Bypass` option applies only to this new PowerShell process. It allows the signed-off recovery script to run when Windows blocks direct `.ps1` execution, without permanently changing the system execution policy.

The setup script validates that the dump contains exactly the `somanath` master database and one `somanath20YY` financial-year database. It reads the existing legacy MySQL credential from the deployed backend configuration and does not prompt for it. Existing tables with the same names can be replaced by the dump, so verify that the correct backup was selected before continuing.

After restoration, complete the post-restore acceptance checklist in `Installation` before using the standby computer for live billing.
