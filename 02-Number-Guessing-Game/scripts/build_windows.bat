@echo off
setlocal
cd /d "%~dp0.." || exit /b 1

set "GAME_PYTHON=.venv\Scripts\python.exe"
if not exist "%GAME_PYTHON%" (
    echo Create the virtual environment first: python -m venv .venv
    exit /b 1
)

"%GAME_PYTHON%" -m pip install -r requirements.txt pyinstaller || exit /b 1
"%GAME_PYTHON%" -m PyInstaller --noconfirm --clean --onefile --windowed --name NumberGuessingGame --collect-all kivy main.py || exit /b 1
if not exist "builds\windows\." mkdir "builds\windows" || exit /b 1
copy /Y "dist\NumberGuessingGame.exe" "builds\windows\NumberGuessingGame.exe" || exit /b 1
