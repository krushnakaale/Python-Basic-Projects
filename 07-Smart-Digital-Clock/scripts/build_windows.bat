@echo off
cd /d "%~dp0.."
python -m pip install -r requirements.txt pyinstaller || exit /b 1
python -m PyInstaller --noconfirm --onefile --windowed --collect-all tzdata --name SmartDigitalClock --distpath builds/windows main.py
