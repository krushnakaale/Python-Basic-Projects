@echo off
cd /d "%~dp0.."
python -m pip install -r requirements.txt pyinstaller || exit /b 1
python -m PyInstaller --noconfirm --onefile --windowed --name SmartTodo main.py || exit /b 1
if not exist builds\windows mkdir builds\windows
copy /Y dist\SmartTodo.exe builds\windows\SmartTodo.exe
