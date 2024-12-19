@echo off

goto :init

setlocal

@REM @echo %__THIS_HOME%
@REM py %__THIS_HOME%\scripts\thing.py

:missing_argument
  @echo.
  @echo Missing required argument: eventDate
  @echo.
  goto :eof

:init
  set "__EVENT_DATE="
  set "__THIS_PATH=%~dp0"
  set "__SOURCE_PATH=%cd%"

:parse
  if "%~1"=="" goto :validate
  if not defined __EVENT_DATE set "__EVENT_DATE=%1" & shift & goto :parse

:validate
  if not defined __EVENT_DATE call :missing_argument & goto :end

:main
  @echo.
  @echo Running Invoice Data script for event date %__EVENT_DATE%
  @echo.
  py "%__THIS_PATH%scripts\invoice_data.py" --eventDate "%__EVENT_DATE%" --sourcePath "%__SOURCE_PATH%"

:end
  call :cleanup
  exit /B

:cleanup


endlocal
