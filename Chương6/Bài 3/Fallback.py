import time
import random

# Máy chủ DNS và trạng thái
dns_servers = {
    "dns_primary": {"status": True, "domains": {"example.com": "192.0.2.1"}},
    "dns_secondary": {"status": True, "domains": {"example.com": "192.0.2.2"}},
    "dns_backup_1": {"status": True, "domains": {"myorg.org": "192.0.2.3"}},
}

# Cờ thống kê
fallback_count = 0
primary_failures = 0

# Thiết lập timeout
DEFAULT_TIMEOUT = 2

# Mô phỏng lỗi máy chủ chính với xác suất hoặc cờ thủ công
simulate_random_fail = False
failure_chance = 0.3  # 30%

# Ghi log
def log(msg):
    print(f"[LOG] {msg}")

def resolve_from_server(server_name, domain, timeout=DEFAULT_TIMEOUT):
    server = dns_servers[server_name]
    if not server['status']:
        raise ConnectionError(f"{server_name} is DOWN")
    
    # Nếu bật mô phỏng ngẫu nhiên → xác suất bị lỗi
    if server_name == "dns_primary" and simulate_random_fail:
        if random.random() < failure_chance:
            raise TimeoutError("Timeout from primary server")
    
    time.sleep(timeout)  # Mô phỏng độ trễ phản hồi

    # Trả về nếu có domain
    if domain in server['domains']:
        return server['domains'][domain]
    else:
        raise ValueError(f"{domain} not found on {server_name}")

# Phân giải tên miền với fallback
def resolve_domain(domain):
    global fallback_count, primary_failures

    servers = list(dns_servers.keys())

    for idx, server_name in enumerate(servers):
        try:
            ip = resolve_from_server(server_name, domain)
            print(f"Resolved from {server_name}: {domain} → {ip}")
            if idx != 0:
                fallback_count += 1
            return ip
        except Exception as e:
            if server_name == "dns_primary":
                primary_failures += 1
            log(f"{server_name} failed: {e}")

    print("Domain not found or all servers failed.")
    return None

# Menu bật/tắt máy chủ
def toggle_server():
    print("\nTrạng thái hiện tại:")
    for name, info in dns_servers.items():
        print(f" - {name}: {'ON' if info['status'] else 'OFF'}")

    name = input("Nhập tên máy chủ muốn bật/tắt: ").strip()
    if name in dns_servers:
        dns_servers[name]['status'] = not dns_servers[name]['status']
        print(f"Đã chuyển {name} sang trạng thái {'ON' if dns_servers[name]['status'] else 'OFF'}")
    else:
        print("Máy chủ không tồn tại.")

# Menu CLI
def menu():
    global simulate_random_fail

    while True:
        print("\n===== DNS Fallback Simulator =====")
        print("1. Phân giải tên miền")
        print("2. Bật/tắt máy chủ")
        print("3. Bật/tắt mô phỏng lỗi ngẫu nhiên DNS chính")
        print("4. Xem thống kê lỗi")
        print("5. Thoát")
        choice = input("→ Chọn chức năng (1-5): ")

        if choice == '1':
            domain = input("Nhập domain: ").strip()
            resolve_domain(domain)
        elif choice == '2':
            toggle_server()
        elif choice == '3':
            simulate_random_fail = not simulate_random_fail
            print(f"Mô phỏng lỗi ngẫu nhiên: {'BẬT' if simulate_random_fail else 'TẮT'}")
        elif choice == '4':
            print("\nThống kê:")
            print(f" - Số lần DNS chính thất bại: {primary_failures}")
            print(f" - Số lần fallback sang server khác: {fallback_count}")
        elif choice == '5':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

# Khởi động chương trình
if __name__ == "__main__":
    menu()
