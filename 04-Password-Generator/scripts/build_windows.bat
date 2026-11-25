@echo off
cd /d "%~dp0.."
python -m pip install pyinstaller || exit /b 1
python -m PyInstaller --noconfirm --clean --onefile --windowed --name PasswordGenerator --distpath builds/windows main.py || exit /b 1
