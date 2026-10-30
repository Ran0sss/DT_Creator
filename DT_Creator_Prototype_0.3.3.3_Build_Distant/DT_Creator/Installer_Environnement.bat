@echo off
setlocal EnableExtensions
cd /d "%~dp0"
title DT Creator - Preparation environnement

echo === DT Creator : preparation de l'environnement local ===
echo.

REM Si l'environnement virtuel existe deja, ne pas le recreer.
if exist ".venv\Scripts\python.exe" goto install

REM Detecter des installations usuelles, y compris Anaconda de developpement.
set "BASE_PY="
for %%P in (
  "C:\Anaconda3\python.exe"
  "%LOCALAPPDATA%\Programs\Python\Python312\python.exe"
  "%LOCALAPPDATA%\Programs\Python\Python311\python.exe"
  "C:\Python312\python.exe"
  "C:\Python311\python.exe"
) do (
  if not defined BASE_PY if exist "%%~P" set "BASE_PY=%%~P"
)

REM Puis essayer le lanceur Windows py.
if not defined BASE_PY (
  where py >nul 2>nul
  if not errorlevel 1 (
    py -3.12 -c "import sys" >nul 2>nul
    if not errorlevel 1 set "BASE_PY=py -3.12"
    if not defined BASE_PY (
      py -3.11 -c "import sys" >nul 2>nul
      if not errorlevel 1 set "BASE_PY=py -3.11"
    )
  )
)

REM Enfin tenter python dans PATH.
if not defined BASE_PY (
  where python >nul 2>nul
  if not errorlevel 1 set "BASE_PY=python"
)

if not defined BASE_PY (
  echo Python n'a pas ete trouve automatiquement.
  echo.
  echo Si Anaconda est installe, ouvrez Anaconda Prompt et tapez :
  echo   where python
  echo Copiez le chemin du python.exe, puis relancez ce setup apres
  echo avoir renseigne BASE_PY dans ce fichier si besoin.
  echo.
  echo Sinon installez Python 3.11 ou 3.12 depuis python.org.
  pause
  exit /b 1
)

echo Python de base detecte : %BASE_PY%
echo Creation de l'environnement isole .venv...
%BASE_PY% -m venv .venv
if errorlevel 1 (
  echo Creation .venv impossible avec ce Python.
  echo Si la source est Anaconda, assurez-vous que le module venv est disponible.
  pause
  exit /b 1
)

:install
echo Installation des dependances dans .venv...
".venv\Scripts\python.exe" -m pip install --upgrade pip
if errorlevel 1 goto error
".venv\Scripts\python.exe" -m pip install -r requirements.txt
if errorlevel 1 goto error
echo.
echo Environnement DT Creator pret.
echo Lancez Lancer_DT.bat.
pause
exit /b 0

:error
echo.
echo Echec de preparation. Verifiez la connexion Internet puis relancez.
pause
exit /b 1
