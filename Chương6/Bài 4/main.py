import time
from server import setup_dns_system

def main():
    root_server = setup_dns_system()

    while True:
        print("\n--- DNS Resolver Simulator ---")
        print("1. Nhập tên miền để phân giải")
        print("2. In cache từng máy chủ")
        print("3. Flush cache tất cả")
        print("0. Thoát")
        choice = input("Chọn: ")

        match choice:
            case "1":
                domain = input("Nhập tên miền (vd: www.example.com): ").strip()
                start = time.time()
                ip = root_server.resolve(domain)
                duration = time.time() - start
                if ip:
                    print(f"→ IP: {ip} (Thời gian: {duration:.4f}s)")
                else:
                    print("→ Không tìm thấy tên miền.")
            case "2":
                root_server.print_cache()
                for tld in root_server.delegates.values():
                    tld.print_cache()
                    for auth in tld.delegates.values():
                        auth.print_cache()
            case "3":
                root_server.flush_cache()
                for tld in root_server.delegates.values():
                    tld.flush_cache()
                    for auth in tld.delegates.values():
                        auth.flush_cache()
                print("→ Đã flush cache tất cả.")
            case "0":
                print("Thoát chương trình.")
                break
            case _:
                print("Lựa chọn không hợp lệ!")

if __name__ == "__main__":
    main()
