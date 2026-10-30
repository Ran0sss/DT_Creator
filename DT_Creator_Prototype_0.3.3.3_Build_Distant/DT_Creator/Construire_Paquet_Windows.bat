@echo off
setlocal
cd /d "%~dp0"
title DT Creator - Construction EXE

if not exist ".venv\Scripts\python.exe" (
  echo Lancez d'abord Installer_Environnement.bat.
  pause
  exit /b 1
)

".venv\Scripts\python.exe" -m pip install --upgrade pyinstaller
if errorlevel 1 goto error

".venv\Scripts\python.exe" -m PyInstaller --noconfirm --clean --onedir --name DT_Creator --collect-all streamlit --collect-all altair --collect-all pyarrow --add-data "dt_creator;dt_creator" dt_creator\launcher.py
if errorlevel 1 goto error

echo.
echo Construction terminee : dist\DT_Creator
echo Pour diffuser : distribuez le dossier dist\DT_Creator complet.
echo L'executable est dist\DT_Creator\DT_Creator.exe
pause
exit /b 0

:error
echo.
echo Echec de construction. Voir les messages precedents.
pause
exit /b 1
