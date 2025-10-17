#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Multi-Device Screen Display using Scrcpy
Hiển thị màn hình nhiều thiết bị Android cùng lúc qua USB
"""

import subprocess
import threading
import time
import tkinter as tk
from tkinter import ttk, messagebox
import os
import sys


class MultiScrcpyManager:
    def __init__(self):
        self.devices = []
        self.processes = {}
        self.root = tk.Tk()
        self.root.title("Multi-Device Screen Display")
        self.root.geometry("800x600")

        # Tạo giao diện
        self.create_gui()

        # Kiểm tra dependencies
        self.check_dependencies()

    def create_gui(self):
        """Tạo giao diện người dùng"""
        # Frame chính
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

        # Tiêu đề
        title_label = ttk.Label(main_frame, text="Multi-Device Android Screen Display",
                               font=("Arial", 16, "bold"))
        title_label.grid(row=0, column=0, columnspan=2, pady=10)

        # Nút refresh thiết bị
        self.refresh_btn = ttk.Button(main_frame, text="Tìm Thiết Bị",
                                     command=self.refresh_devices)
        self.refresh_btn.grid(row=1, column=0, pady=10)

        # Nút dừng tất cả màn hình
        self.stop_all_btn = ttk.Button(main_frame, text="Dừng Tất Cả Màn Hình",
                                     command=self.stop_all_displays)
        self.stop_all_btn.grid(row=1, column=2, pady=10)

        # Danh sách thiết bị
        self.devices_frame = ttk.LabelFrame(main_frame, text="Thiết Bị Đã Kết Nối", padding="10")
        self.devices_frame.grid(row=2, column=0, columnspan=2, sticky=(tk.W, tk.E, tk.N, tk.S), pady=10)

        # Scrollbar cho danh sách thiết bị
        self.devices_canvas = tk.Canvas(self.devices_frame)
        scrollbar = ttk.Scrollbar(self.devices_frame, orient="vertical", command=self.devices_canvas.yview)
        self.scrollable_frame = ttk.Frame(self.devices_canvas)

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.devices_canvas.configure(scrollregion=self.devices_canvas.bbox("all"))
        )

        self.devices_canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")
        self.devices_canvas.configure(yscrollcommand=scrollbar.set)

        self.devices_canvas.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        scrollbar.grid(row=0, column=1, sticky=(tk.N, tk.S))

        # Frame cho các thiết bị
        self.device_frames = []

        # Log area
        log_frame = ttk.LabelFrame(main_frame, text="Log", padding="10")
        log_frame.grid(row=3, column=0, columnspan=2, sticky=(tk.W, tk.E), pady=10)

        self.log_text = tk.Text(log_frame, height=10, width=80)
        self.log_text.grid(row=0, column=0, sticky=(tk.W, tk.E))

        scrollbar_log = ttk.Scrollbar(log_frame, orient="vertical", command=self.log_text.yview)
        scrollbar_log.grid(row=0, column=1, sticky=(tk.N, tk.S))
        self.log_text.configure(yscrollcommand=scrollbar_log.set)

        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(1, weight=1)
        main_frame.rowconfigure(2, weight=1)

        # Auto refresh mỗi 5 giây
        self.root.after(5000, self.auto_refresh)

    def check_dependencies(self):
        """Kiểm tra các dependencies cần thiết"""
        required_commands = ['adb', 'scrcpy']
        missing_commands = []

        for cmd in required_commands:
            if not self.is_command_available(cmd):
                missing_commands.append(cmd)

        if missing_commands:
            message = f"Thiếu các công cụ cần thiết: {', '.join(missing_commands)}\n\n"
            message += "Vui lòng cài đặt:\n"
            message += "1. Android SDK Platform Tools (adb)\n"
            message += "2. Scrcpy (https://github.com/Genymobile/scrcpy)"

            messagebox.showerror("Lỗi Dependencies", message)
            self.log_message(f"Lỗi: Thiếu {', '.join(missing_commands)}")
            return False

        self.log_message("Tất cả dependencies đã sẵn sàng")
        return True

    def is_command_available(self, command):
        """Kiểm tra xem lệnh có khả dụng không"""
        try:
            subprocess.run([command, '--version'], capture_output=True, check=True)
            return True
        except (subprocess.CalledProcessError, FileNotFoundError):
            return False

    def is_device_ready(self, device_id):
        """Kiểm tra xem thiết bị có sẵn sàng không"""
        try:
            # Kiểm tra thiết bị có trong danh sách adb không
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True, timeout=5)
            devices = [line.split('\t')[0] for line in result.stdout.strip().split('\n')[1:] if line.strip() and not line.strip().startswith('*') and line.split('\t')[0] == device_id]
            if not devices:
                return False

            # Kiểm tra kết nối cơ bản
            subprocess.run(['adb', '-s', device_id, 'shell', 'echo', 'test'], capture_output=True, check=True, timeout=5)
            return True
        except (subprocess.CalledProcessError, subprocess.TimeoutExpired, FileNotFoundError):
            return False

    def refresh_devices(self):
        """Làm mới danh sách thiết bị"""
        self.log_message("Đang tìm thiết bị...")
        self.devices = self.get_connected_devices()

        if not self.devices:
            self.log_message("Không tìm thấy thiết bị nào được kết nối qua USB")
            messagebox.showinfo("Thông Báo", "Không tìm thấy thiết bị Android nào được kết nối qua USB")
        else:
            self.log_message(f"Tìm thấy {len(self.devices)} thiết bị")
            self.update_devices_list()

    def get_connected_devices(self):
        """Lấy danh sách thiết bị được kết nối"""
        try:
            result = subprocess.run(['adb', 'devices'], capture_output=True, text=True, check=True)
            devices = []

            for line in result.stdout.strip().split('\n')[1:]:  # Bỏ qua dòng đầu
                if line.strip() and not line.strip().startswith('*'):
                    device_id = line.split('\t')[0]
                    if device_id:
                        devices.append(device_id)

            return devices
        except subprocess.CalledProcessError as e:
            self.log_message(f"Lỗi khi lấy danh sách thiết bị: {e}")
            return []

    def update_devices_list(self):
        """Cập nhật giao diện danh sách thiết bị"""
        # Xóa các frame cũ
        for frame in self.device_frames:
            frame.destroy()
        self.device_frames = []

        # Tạo frame mới cho mỗi thiết bị
        for i, device_id in enumerate(self.devices):
            device_frame = ttk.LabelFrame(self.scrollable_frame, text=f"Thiết Bị {i+1}: {device_id}", padding="5")
            device_frame.grid(row=i, column=0, sticky=(tk.W, tk.E), pady=5, padx=5)

            # Thông tin thiết bị
            try:
                # Lấy tên thiết bị
                result = subprocess.run(['adb', '-s', device_id, 'shell', 'getprop', 'ro.product.model'],
                                      capture_output=True, text=True, check=True)
                device_name = result.stdout.strip()
            except:
                device_name = "Không xác định"

            name_label = ttk.Label(device_frame, text=f"Tên: {device_name}")
            name_label.grid(row=0, column=0, sticky=tk.W)

            # Nút hiển thị màn hình
            display_btn = ttk.Button(device_frame, text="Hiển Thị Màn Hình",
                                   command=lambda d=device_id: self.display_single_screen(d))
            display_btn.grid(row=1, column=0, pady=5)

            # Nút dừng hiển thị
            stop_btn = ttk.Button(device_frame, text="Dừng Hiển Thị",
                                 command=lambda d=device_id: self.stop_display(d))
            stop_btn.grid(row=1, column=1, pady=5)

            self.device_frames.append(device_frame)

    def display_all_screens(self):
        """Hiển thị tất cả màn hình thiết bị"""
        if not self.devices:
            messagebox.showwarning("Cảnh Báo", "Không có thiết bị nào được kết nối")
            return

        # Giới hạn số thiết bị để tránh overload (có thể cấu hình từ config)
        max_devices = getattr(self, 'max_concurrent_devices', 5)
        if len(self.devices) > max_devices:
            messagebox.showwarning("Cảnh Báo", f"Quá nhiều thiết bị ({len(self.devices)}). Chỉ hiển thị tối đa {max_devices} thiết bị đầu tiên.")
            devices_to_display = self.devices[:max_devices]
        else:
            devices_to_display = self.devices

        for i, device_id in enumerate(devices_to_display):
            # Thêm delay nhỏ giữa các lần khởi chạy để tránh xung đột
            if i > 0:
                time.sleep(2)  # Delay 2 giây giữa mỗi thiết bị
            self.display_single_screen(device_id)

    def display_single_screen(self, device_id):
        """Hiển thị màn hình của một thiết bị"""
        if device_id in self.processes:
            messagebox.showinfo("Thông Báo", f"Màn hình của thiết bị {device_id} đang được hiển thị")
            return

        # Kiểm tra trạng thái thiết bị trước khi khởi chạy
        if not self.is_device_ready(device_id):
            self.log_message(f"Thiết bị {device_id} không sẵn sàng để hiển thị màn hình")
            messagebox.showerror("Lỗi", f"Thiết bị {device_id} không sẵn sàng. Vui lòng kiểm tra kết nối USB.")
            return

        try:
            # Chạy scrcpy cho thiết bị cụ thể
            process = subprocess.Popen(['scrcpy', '-s', device_id, '--window-title', f'Android-{device_id}'],
                                    stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

            self.processes[device_id] = process
            self.log_message(f"Đã bắt đầu hiển thị màn hình cho thiết bị {device_id}")

            # Theo dõi tiến trình trong thread riêng
            threading.Thread(target=self.monitor_process, args=(device_id, process), daemon=True).start()

        except Exception as e:
            self.log_message(f"Lỗi khi hiển thị màn hình thiết bị {device_id}: {e}")
            messagebox.showerror("Lỗi", f"Không thể hiển thị màn hình thiết bị {device_id}: {e}")

    def stop_display(self, device_id):
        """Dừng hiển thị màn hình của một thiết bị"""
        if device_id not in self.processes:
            messagebox.showinfo("Thông Báo", f"Màn hình của thiết bị {device_id} không đang được hiển thị")
            return

        try:
            process = self.processes[device_id]
            process.terminate()

            # Đợi tiến trình kết thúc
            try:
                process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                process.kill()

            del self.processes[device_id]
            self.log_message(f"Đã dừng hiển thị màn hình thiết bị {device_id}")

        except Exception as e:
            self.log_message(f"Lỗi khi dừng hiển thị thiết bị {device_id}: {e}")

    def stop_all_displays(self):
        """Dừng hiển thị tất cả màn hình"""
        if not self.processes:
            messagebox.showinfo("Thông Báo", "Không có màn hình nào đang được hiển thị")
            return

        for device_id in list(self.processes.keys()):
            self.stop_display(device_id)
        self.log_message("Đã dừng tất cả màn hình")

    def monitor_process(self, device_id, process):
        """Theo dõi tiến trình scrcpy"""
        try:
            stdout, stderr = process.communicate()

            if process in self.processes:
                del self.processes[device_id]

            if process.returncode == 0:
                self.log_message(f"Tiến trình scrcpy cho thiết bị {device_id} kết thúc bình thường")
            else:
                self.log_message(f"Tiến trình scrcpy cho thiết bị {device_id} kết thúc với mã lỗi {process.returncode}")
                if stderr:
                    self.log_message(f"Lỗi stderr từ thiết bị {device_id}: {stderr[:200]}...")  # Log một phần để tránh quá dài

        except Exception as e:
            self.log_message(f"Lỗi khi theo dõi tiến trình thiết bị {device_id}: {e}")

    def log_message(self, message):
        """Ghi log"""
        timestamp = time.strftime("%H:%M:%S")
        self.log_text.insert(tk.END, f"[{timestamp}] {message}\n")
        self.log_text.see(tk.END)

    def auto_refresh(self):
        """Tự động làm mới thiết bị mỗi 5 giây"""
        try:
            current_devices = set(self.get_connected_devices())
            existing_devices = set(self.devices)

            if current_devices != existing_devices:
                self.refresh_devices()
        except Exception as e:
            self.log_message(f"Lỗi khi tự động làm mới: {e}")

        # Lên lịch cho lần tiếp theo
        self.root.after(5000, self.auto_refresh)

    def run(self):
        """Chạy ứng dụng"""
        self.root.mainloop()


def main():
    """Hàm chính"""
    try:
        manager = MultiScrcpyManager()
        manager.run()
    except KeyboardInterrupt:
        print("\nỨng dụng đã được dừng bởi người dùng")
    except Exception as e:
        print(f"Lỗi không mong muốn: {e}")


if __name__ == "__main__":
    main()
