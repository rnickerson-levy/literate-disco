@echo off

goto :init

:header
  echo %__NAME% v%__VERSION%
  echo This batch file will attempt to set up the InvoiceDataApp
  echo folders and scripts.
  echo.
  goto :eof

:usage
  echo USAGE:
  echo   %__BAT_NAME% [flags] "required argument" "optional argument" 
  echo.
  echo.  /?, --help           shows this help
  echo.  /v, --version        shows the version
  echo.  /e, --verbose        shows detailed output
  goto :eof

:version
  if "%~1"=="full" call :header & goto :eof
  echo %__VERSION%
  goto :eof

:missing_argument
  call :header
  call :usage
  echo.
  echo ****                                   ****
  echo ****    MISSING "REQUIRED ARGUMENT"    ****
  echo ****                                   ****
  echo.
  goto :eof

:init
  set "__NAME=%~n0"
  set "__VERSION=0.1"

  set "__BAT_FILE=%~0"
  set "__BAT_PATH=%~dp0"
  set "__BAT_NAME=%~nx0"

  set __DEFAULT_APP_ROOT=%localappdata%
  set __DEFAULT_APP_NAME=InvoiceDataApp

  set __APP_ROOT=%__DEFAULT_APP_ROOT%
  set __APP_NAME=%__DEFAULT_APP_NAME%

:parse
  if "%~1"=="" goto :validate

  if /i "%~1"=="/?"         call :header & call :usage "%~2" & goto :end
  if /i "%~1"=="-?"         call :header & call :usage "%~2" & goto :end
  if /i "%~1"=="--help"     call :header & call :usage "%~2" & goto :end

  if /i "%~1"=="/v"         call :version      & goto :end
  if /i "%~1"=="-v"         call :version      & goto :end
  if /i "%~1"=="--version"  call :version full & goto :end

  if /i "%~1"=="/r"         set "__APP_ROOT=%~2" & shift & shift & goto :parse
  if /i "%~1"=="-r"         set "__APP_ROOT=%~2" & shift & shift & goto :parse
  if /i "%~1"=="/--root"    set "__APP_ROOT=%~2" & shift & shift & goto :parse

  if /i "%~1"=="/n"         set "__APP_NAME=%~2" & shift & shift & goto :parse
  if /i "%~1"=="-n"         set "__APP_NAME=%~2" & shift & shift & goto :parse
  if /i "%~1"=="/--name"    set "__APP_NAME=%~2" & shift & shift & goto :parse

  shift
  goto :parse

:validate
  @REM Do nothing for now...

:main
  @echo.
  @echo.

  @echo ==============================================
  @echo ==      RUNNING INVOICE DATA APP SETUP      ==
  @echo ==============================================
  @echo.

  @REM choice /c yn /m "Do you want to install the Invoice Data scripts? "

  @REM if %ERRORLEVEL%==2 (
  @REM   @echo.
  @REM   @echo Exiting...
  @REM   @echo.
  @REM   @echo.
  @REM   goto :end
  @REM )

  @echo Using values:
  @echo.  Application Name:        "%__APP_NAME%"
  @echo.  Application Home Folder: "%__APP_ROOT%\%__APP_NAME%"

  @echo.

  @echo Setting up application home folder...
  @if not exist "%__APP_ROOT%\%__APP_NAME%" (
    @mkdir "%__APP_ROOT_FOLDER%\%__APP_NAME%" > nul
    @echo.  Folder created ("%__APP_ROOT%\%__APP_NAME%")
  ) else (
    @echo.  Folder already exists ("%__APP_ROOT%\%__APP_NAME%")
  )

  @echo.

  @echo Copying files...
  robocopy ".\scripts" "%__APP_ROOT%\%__APP_NAME%\scripts" /E /is /it > nul
  @echo.  ".\scripts" copied
  robocopy %__BAT_PATH% %__APP_ROOT%\%__APP_NAME%\ invoice-data.bat /is /it > nul
  @echo.  ".\invoice-data.bat" copied
  robocopy %__BAT_PATH% %__APP_ROOT%\%__APP_NAME%\ setup.bat /is /it > nul
  @echo.  ".\setup.bat" copied

  @echo.

  @echo +++++++++++++++++++++++++++++++++++++++++++++++
  @echo YOU MUST UPDATE YOUR PATH ENVIRONMENT VARIABLE
  @echo TO CONTAIN THE FOLDER LISTED HERE:
  @echo.
  @echo %__APP_ROOT%\%__APP_NAME%
  @echo.
  @echo Highlight and copy this path to paste into
  @echo the Windows System Environment variables dialog
  @echo +++++++++++++++++++++++++++++++++++++++++++++++

  @echo.
  @echo.

  pause

  @echo.
  @echo.

  goto :end

:end
  call :cleanup
  exit /B

:cleanup
  set "__NAME="
  set "__VERSION="
  set "__YEAR="

  set "__APP_NAME="
  set "__APP_ROOT_FOLDER="
  set "__DEFAULT_APP_NAME="
  @REM set "__APP_HOME="


@REM @if exist %__APP_HOME% (
@REM   @echo FOUND
@REM ) else (
@REM   @echo NOT FOUND
@REM )

@REM :one
@REM   echo. ONE

@REM :two
@REM   echo. TWO
@REM   if not defined PATH goto :eof

@REM :three
@REM   echo. THREE

