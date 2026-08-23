# Hosangadi2.0

## Recovery and installation

- See [`Installation`](Installation) for complete system setup, scheduled tasks and the post-restore acceptance checklist.
- See [`RESTORE_FROM_PENDRIVE.md`](RESTORE_FROM_PENDRIVE.md) for the exact command used to restore the master and current financial-year databases from a selected pendrive backup.

### Quick standby-system database replacement

When the standby computer is already fully configured, place exactly two completed `.sql` files beside `restore_backup_system.bat` and double-click the BAT file:

- The smaller file must contain exactly `somanath` plus one current `somanath20YY` database.
- The larger file must be the March 31 full backup and contain `somanath` plus more than one financial-year database.

The launcher requests Administrator permission, validates both files and asks the operator to type `RESTORE`. It stops PM2, drops only existing Hosangadi databases, restores the full-history dump first, restores the latest two-database dump second so its master/current data wins, validates all restored schemas and tables, then restarts and saves PM2. Validation failures occur before database deletion. MySQL internal system schemas are never dropped.

### Features availble in Hosangadi2.0

![ezgif### H3 com-gif-maker](https://user-images.githubusercontent.com/90487058/177008011-dccf6922-fe01-434d-a5c7-92195e7a6d51.gif)

### Demonstration of Sales Entry in Hosangadi2.0


https://user-images.githubusercontent.com/90487058/177008258-7276f04e-4962-4d59-a173-29e7f41e50d0.mp4



### Demonstration of Sales Entry in Hosangadi1.0


https://user-images.githubusercontent.com/90487058/177008252-04cbc943-ef1c-4649-b1f6-68116a69d74b.mp4

