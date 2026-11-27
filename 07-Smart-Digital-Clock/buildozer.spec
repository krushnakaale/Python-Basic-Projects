[app]
title = Smart Digital Clock
package.name = smartdigitalclock
package.domain = org.krushnakaale
source.dir = .
source.include_exts = py,json,kv
source.exclude_dirs = tests,scripts,builds,.venv,.venv-linux,.buildozer,dist,build
version = 1.0
requirements = python3,kivy,tzdata
orientation = portrait
fullscreen = 0
android.api = 35
android.minapi = 23
android.archs = arm64-v8a
[buildozer]
log_level = 2
warn_on_root = 1
