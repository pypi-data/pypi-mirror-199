@echo off
cd C:\Users\danny\source\repos\Python\FluxFrameworkPackage

echo Removing Old Build...

del /q dist\*

@echo Incrementing Version Number...

set /p Build=<version.txt
set /p OldBuild=<version.txt
for /f "tokens=1-3 delims=. " %%a in ("%Build%") do (
set Major=%%a
set Minor=%%b
set Hotfix=%%c
)
SET /a Hotfix+=1
REM echo Major=%Major%
REM echo Minor=%Minor%
REM echo Hotfix=%Hotfix%
set Build=%Major%.%Minor%.%Hotfix%
>version.txt echo %Build%

@echo Updating Version Number...

setlocal enableextensions disabledelayedexpansion

set "textFile=pyproject.toml"
set "search=%OldBuild%"
set "replace=%Build%"

REM echo %textFile%
REM echo %OldBuild%
REM echo %Build%

for /f "delims=" %%i in ('type "%textFile%" ^& break ^> "%textFile%" ') do (
	set "line=%%i"
	setlocal enabledelayedexpansion
	>>"%textFile%" echo(!line:%search%=%replace%!
	endlocal
)

set "PyPiToken=pypi-AgEIcHlwaS5vcmcCJGY4NzAzNWY2LWM5ODQtNDFlNC04OTA2LTMzNTczMWE0ZjVmYQACKlszLCI2ZmU0YmVmOS0xYWRkLTRlZTctOWJmNS1lMWMwM2I5OWQyNGUiXQAABiBQSvikYzn_DHaZYz3S0YUxlcIakJMLNxd_grr7VjbOZQ"

@echo Building Package...

py -m build

@echo Uploading Package...

py -m twine upload -u __token__ -p %PyPiToken%  dist/*

@echo Update Complete. To install/update the package run the following command:
@echo py -m pip install FluxFramework==%Build%