#!/usr/bin/env bash
set -euo pipefail
cd "$(dirname "$0")/.."
buildozer -v android debug
mkdir -p builds/android
cp bin/*.apk builds/android/
