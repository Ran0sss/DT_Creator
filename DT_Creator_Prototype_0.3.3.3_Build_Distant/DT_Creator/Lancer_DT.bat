@echo off
setlocal
cd /d "%~dp0"
title DT Creator

REM Preferer la version Windows autonome si elle a ete construite/cop iee.
if exist "%~dp0DT_Creator\DT_Creator.exe" (
  start "" "%~dp0DT_Creator\DT_Creator.exe"
  exit /b 0
)

if not exist ".venv\Scripts\python.exe" (
  echo Environnement absent. Lancez d'abord Installer_Environnement.bat.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" -m streamlit run "%~dp0dt_creator\app.py" --server.address 127.0.0.1 --browser.gatherUsageStats false
if errorlevel 1 (
  echo.
  echo Echec du lancement. Essayez Installer_Environnement.bat.
  pause
)
endlocal
