@echo off
cd /d "%~dp0.."
python -m pip install pyinstaller
python -m PyInstaller --noconfirm --clean --onefile --windowed --name RockPaperScissors --collect-all kivy main.py
if errorlevel 1 exit /b 1
if not exist "builds\windows" mkdir "builds\windows"
copy /Y "dist\RockPaperScissors.exe" "builds\windows\RockPaperScissors.exe"
echo Build complete: builds\windows\RockPaperScissors.exe
