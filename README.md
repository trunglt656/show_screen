# Multi-Device Android Screen Display

Chương trình hiển thị màn hình nhiều thiết bị Android cùng lúc qua USB sử dụng Scrcpy.

## Tính Năng

- **Phát hiện thiết bị tự động**: Tự động tìm các thiết bị Android được kết nối qua USB
- **Hiển thị đa màn hình**: Có thể hiển thị màn hình nhiều thiết bị cùng lúc
- **Giao diện thân thiện**: Giao diện GUI đơn giản và dễ sử dụng
- **Quản lý thiết bị**: Có thể bật/tắt hiển thị màn hình từng thiết bị riêng biệt
- **Tự động làm mới**: Tự động kiểm tra thiết bị mới mỗi 5 giây

## Yêu Cầu Hệ Thống

### Phần mềm cần thiết:

1. **Python 3.6+**
   - Tải về tại: https://python.org

2. **Android SDK Platform Tools (ADB)**
   - Tải về tại: https://developer.android.com/studio/releases/platform-tools
   - Đảm bảo `adb` có trong PATH hệ thống

3. **Scrcpy**
   - Tải về tại: https://github.com/Genymobile/scrcpy
   - Có thể cài đặt qua:
     - Windows: Chocolatey (`choco install scrcpy`)
     - Linux: Snap (`sudo snap install scrcpy`) hoặc APT
     - macOS: Homebrew (`brew install scrcpy`)

### Thiết bị Android:

- Thiết bị Android có USB Debugging được bật
- Kết nối USB với máy tính
- Một số thiết bị cần thêm driver USB

## Cách Bật USB Debugging trên Android

1. Vào **Cài đặt > Giới thiệu về điện thoại**
2. Nhấn 7 lần vào **Số bản build** để bật **Chế độ nhà phát triển**
3. Quay lại **Cài đặt > Tùy chọn nhà phát triển**
4. Bật **USB Debugging**
5. Chấp nhận fingerprint khi kết nối lần đầu

## Cài Đặt và Chạy

### 1. Chuẩn bị môi trường

```bash
# Cài đặt các công cụ cần thiết (Windows)
# 1. Cài đặt Android SDK Platform Tools
# 2. Cài đặt Scrcpy

# Đảm bảo các lệnh sau hoạt động:
adb --version
scrcpy --version
```

### 2. Chạy chương trình

```bash
# Chạy chương trình
python main.py
```

### 3. Sử dụng chương trình

1. **Kết nối thiết bị**: Cắm thiết bị Android qua USB
2. **Tìm thiết bị**: Nhấn nút "Tìm Thiết Bị" hoặc đợi tự động làm mới
3. **Hiển thị màn hình**:
   - Nhấn "Hiển Thị Tất Cả Màn Hình" để hiển thị tất cả thiết bị
   - Hoặc nhấn "Hiển Thị Màn Hình" cho từng thiết bị riêng biệt
4. **Dừng hiển thị**: Nhấn "Dừng Hiển Thị" để tắt màn hình thiết bị

## Cách Sử Dụng

### Giao diện chính:

- **Tìm Thiết Bị**: Quét và liệt kê thiết bị Android được kết nối
- **Hiển Thị Tất Cả Màn Hình**: Khởi chạy scrcpy cho tất cả thiết bị được tìm thấy
- **Danh sách thiết bị**: Hiển thị thông tin từng thiết bị và các nút điều khiển

### Màn hình Scrcpy:

- **Chuột**: Điều khiển như màn hình cảm ứng
- **Bàn phím**: Một số phím tắt có sẵn
- **Cửa sổ**: Có thể thay đổi kích thước và di chuyển
- **Đóng cửa sổ**: Tự động dừng tiến trình scrcpy tương ứng

## Xử Lý Sự Cố

### Lỗi thường gặp:

1. **"Không tìm thấy thiết bị"**
   - Kiểm tra kết nối USB
   - Đảm bảo USB Debugging đã bật
   - Thử rút ra cắm lại cáp USB

2. **"command not found: adb" hoặc "command not found: scrcpy"**
   - Đảm bảo đã cài đặt đúng công cụ
   - Kiểm tra PATH hệ thống
   - Khởi động lại terminal/cmd sau khi cài đặt

3. **"device not found" hoặc lỗi kết nối**
   - Kiểm tra trạng thái thiết bị: `adb devices`
   - Đảm bảo chỉ có một thiết bị được kết nối khi test
   - Thử restart adb server: `adb kill-server && adb start-server`

4. **Màn hình đen hoặc không hiển thị**
   - Kiểm tra kết nối USB
   - Thử chạy `scrcpy` trực tiếp để test
   - Một số thiết bị cần driver USB đặc biệt

### Debug chi tiết:

```bash
# Kiểm tra thiết bị
adb devices

# Test kết nối cơ bản
adb shell "echo 'test'"

# Chạy scrcpy với debug
scrcpy --verbose
```

## Tính Năng Nâng Cao

- **Hiển thị nhiều thiết bị**: Chương trình tự động quản lý nhiều cửa sổ scrcpy
- **Tự động làm mới**: Phát hiện thiết bị mới được kết nối
- **Logging**: Ghi lại hoạt động để debug
- **Giao diện đơn giản**: Dễ sử dụng cho người không chuyên về kỹ thuật

## Giới Hạn

- Chỉ hỗ trợ kết nối qua USB (không hỗ trợ WiFi)
- Cần bật USB Debugging trên thiết bị
- Một số thiết bị có thể cần driver USB đặc biệt
- Hiệu suất phụ thuộc vào sức mạnh máy tính và số lượng thiết bị

## Đóng Góp

Nếu bạn muốn cải thiện chương trình:
1. Tạo issue để báo cáo lỗi hoặc đề xuất tính năng
2. Tạo pull request với code cải tiến

## Giấy Phép

Chương trình này sử dụng các công cụ mã nguồn mở:
- Scrcpy (Apache License 2.0)
- Python tkinter (PSF License)
- ADB (Apache License 2.0)

---

*Tạo bởi: Multi-Device Android Screen Display Tool*
