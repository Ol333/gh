chcp 1251>nul

C:\Users\Olga\Downloads\gikou2_win\gikou<init.txt

Setlocal EnableDelayedExpansion
set counter=0
for /f "delims=" %%i in (input.txt) do (
	echo %%i>>temp_input.txt
	set /a counter=!counter!+1
	if !counter! geq 3 (
	set counter=0
	C:\Users\Olga\Downloads\gikou2_win\gikou<temp_input.txt
	ping -n 1 -w 10000 192.168.254.254 >nul
	del temp_input.txt
	)
)