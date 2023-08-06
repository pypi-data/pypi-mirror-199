cd C:\Users\danny\source\repos\Python\FluxFrameworkPackage
del /q dist\*
set /p Build=<version.txt
set /p OldBuild=<version.txt
FOR /F "tokens=1-3 delims=." %%G IN ("%Build%") DO set /A G=G & set /A H=H & set /A I=I+1
set Build=%G%.%H%.%I%
>version.txt echo %Build%
setlocal enableextensions disabledelayedexpansion

set "textFile=pyproject.toml"
set "search=%OldBuild%"
set "replace=%Build%"

echo %textFile%
echo %OldBuild%
echo %Build%

for /f "delims=" %%i in ('type "%textFile%" ^& break ^> "%textFile%" ') do (
	set "line=%%i"
	setlocal enabledelayedexpansion
	>>"%textFile%" echo(!line:%search%=%replace%!
	endlocal
)
pause