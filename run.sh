#!/bin/bash
# Script chạy Multi-Device Android Screen Display trên Linux/macOS

echo "=== Multi-Device Android Screen Display ==="
echo "Đang kiểm tra dependencies..."

# Kiểm tra Python
if ! command -v python3 &> /dev/null; then
    echo "❌ Lỗi: Python 3 không được tìm thấy!"
    echo "Vui lòng cài đặt Python 3 từ https://python.org"
    exit 1
fi

# Kiểm tra ADB
if ! command -v adb &> /dev/null; then
    echo "❌ Lỗi: ADB không được tìm thấy!"
    echo "Vui lòng cài đặt Android SDK Platform Tools"
    exit 1
fi

# Kiểm tra Scrcpy
if ! command -v scrcpy &> /dev/null; then
    echo "❌ Lỗi: Scrcpy không được tìm thấy!"
    echo "Vui lòng cài đặt Scrcpy từ https://github.com/Genymobile/scrcpy"
    exit 1
fi

echo "✅ Tất cả dependencies đã sẵn sàng!"
echo "Đang khởi chạy chương trình..."

# Chạy chương trình
python3 main.py
