%~d0

cd "%~p0"



IF echo "%username%" == "Администратор"
	start python C:\POU_SQL_Backup\main.py


IF echo "%username%" == "user"
	start python C:\BACKUP\POU_SQL_Backup\main.py