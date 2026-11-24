# Rock Paper Scissors — Python Basic Project 03

A clean, cross-platform Rock Paper Scissors game built with **Python and Kivy**.

## Features

- Professional, minimal light UI
- Play against a computer using randomized choices
- Best-of-3, best-of-5, or best-of-7 matches
- Round-by-round feedback and recent history
- Lifetime match wins/losses saved locally as JSON
- Responsive layout for Windows and Android
- Pure Python game logic with automated tests

## Requirements

- Python 3.10+ recommended
- Kivy (see `requirements.txt`)

## Run on Windows (PowerShell)

```powershell
cd E:\Python-Basic-Projects\Python-Basic-Projects\03-Rock-Paper-Scissors
py -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
python main.py
```

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Build Windows EXE

From an activated Windows Python environment:

```powershell
.\scripts\build_windows.bat
```

Output: `builds/windows/RockPaperScissors.exe`. The Windows build script uses PyInstaller. Antivirus may inspect newly built executables.

## Build Android APK using Kali Linux on WSL2

Android builds require a Linux environment, Java, Buildozer and Android SDK/NDK dependencies. Kali is less commonly tested than Ubuntu for Buildozer, so adjustments may be required. Keep the project in the **Linux home filesystem**, not under `/mnt/e`, during compilation.

```bash
sudo apt update
sudo apt install -y default-jdk git zip unzip python3 python3-venv python3-pip python3-dev build-essential autoconf automake libtool pkg-config cmake libffi-dev libssl-dev zlib1g-dev
mkdir -p ~/Python-Basic-Projects
cp -r /mnt/e/Python-Basic-Projects/Python-Basic-Projects/03-Rock-Paper-Scissors ~/Python-Basic-Projects/
cd ~/Python-Basic-Projects/03-Rock-Paper-Scissors
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install buildozer 'cython<3'
bash scripts/build_android.sh
```

Buildozer downloads the Android toolchain on first use. Additional Kali-specific dependencies may be necessary. Output is copied to `builds/android/` after a successful build. To copy to Windows:

```bash
mkdir -p /mnt/e/Python-Basic-Projects/Python-Basic-Projects/03-Rock-Paper-Scissors/builds/android
cp builds/android/*.apk /mnt/e/Python-Basic-Projects/Python-Basic-Projects/03-Rock-Paper-Scissors/builds/android/
```

**Note:** Source code and build scripts are included; compiled `.exe` and `.apk` are not prebuilt. Validate builds on your own devices.

## Project structure

```text
03-Rock-Paper-Scissors/
├── main.py
├── game_logic.py
├── requirements.txt
├── buildozer.spec
├── README.md
├── .gitignore
├── tests/test_game_logic.py
├── scripts/build_windows.bat
├── scripts/build_android.sh
└── builds/
    ├── windows/
    └── android/
```

## About the Developer

**Krushna Kale** — Python Developer | Software Development Enthusiast | Tech Explorer

I build practical, user-focused software while strengthening my skills in Python, software engineering, automation, AI and cybersecurity. I value clear code, continuous learning and thoughtful problem-solving.

- [GitHub](https://github.com/krushnakaale)
- [LinkedIn](https://www.linkedin.com/in/krushnakaale/)
- [Instagram](https://www.instagram.com/krushna_kaale/)

_LinkedIn and Instagram links are based on the supplied username and have not been independently verified._

© 2026 Krushna Kale. See the parent repository for licensing details.
