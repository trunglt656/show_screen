@echo off
REM Script chạy Multi-Device Android Screen Display trên Windows

echo === Multi-Device Android Screen Display ===
echo Dang kiem tra dependencies...

REM Kiểm tra Python
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Loi: Python khong duoc tim thay!
    echo Vui long cai dat Python 3 tu https://python.org
    pause
    exit /b 1
)

REM Kiểm tra ADB
adb version >nul 2>&1
if errorlevel 1 (
    echo ❌ Loi: ADB khong duoc tim thay!
    echo Vui long cai dat Android SDK Platform Tools
    echo Tai ve tai: https://developer.android.com/studio/releases/platform-tools
    pause
    exit /b 1
)

REM Kiểm tra Scrcpy
scrcpy --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Loi: Scrcpy khong duoc tim thay!
    echo Vui long cai dat Scrcpy tu https://github.com/Genymobile/scrcpy
    pause
    exit /b 1
)

echo ✅ Tat ca dependencies da san sang!
echo Dang khoi chay chuong trinh...
echo.

REM Chạy chương trình
python main.py

pause
