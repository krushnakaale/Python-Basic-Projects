@echo off
cd /d "%~dp0.."
python -m pip install pyinstaller || exit /b 1
python -m PyInstaller --noconfirm --onefile --windowed --name SmartQRGenerator --collect-all kivy --collect-all qrcode main.py || exit /b 1
if not exist builds\windows mkdir builds\windows
copy /Y dist\SmartQRGenerator.exe builds\windows\SmartQRGenerator.exe
