[app]
title = Smart QR Generator
package.name = smartqr
package.domain = org.pythonbasicprojects
source.dir = .
source.include_exts = py,png,kv
source.exclude_dirs = tests,scripts,builds,.venv,.venv-linux,bin
version = 1.0
requirements = python3,kivy,qrcode,pillow
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
[buildozer]
log_level = 2
warn_on_root = 1
