set FILENAME=somanathstores_%DATE%.sql

mysqldump -uroot -pmysqlpassword5 -h localhost --databases somanath somanath2024 > C:\backup\%FILENAME%

xcopy /S /Q /Y /F C:\backup\%FILENAME% D:\backup\

echo "...................................BACKUP AITHU.........................................."

timeout /t 5