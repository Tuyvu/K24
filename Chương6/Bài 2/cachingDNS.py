import time
from collections import OrderedDict

# Cấu hình
CACHE_SIZE = 5  # giới hạn cache
cache = OrderedDict()
stats = {'hit': 0, 'miss': 0}

def resolve_dns(domain):
    print(f"Resolving from network: {domain}")
    time.sleep(1)  # giả lập độ trễ
    ip = f"203.0.113.{hash(domain) % 100 + 1}"  # IP giả lập
    return ip

# Hàm kiểm tra cache và phân giải
def query(domain, ttl):
    current_time = time.time()
    
    # Kiểm tra cache
    if domain in cache:
        ip, expire_time = cache[domain]
        if current_time < expire_time:
            print(f"Cache HIT: {domain} → {ip}")
            cache.move_to_end(domain)
            stats['hit'] += 1
            return ip
        else:
            print(f"Cache EXPIRED for {domain}")
            del cache[domain]

    # Phân giải mới
    stats['miss'] += 1
    ip = resolve_dns(domain)
    expire_time = current_time + ttl
    
    # Nếu cache đầy → Xoá theo LRU
    if len(cache) >= CACHE_SIZE:
        evicted = cache.popitem(last=False)
        print(f"LRU removed: {evicted[0]}")

    cache[domain] = (ip, expire_time)
    print(f"Cached: {domain} → {ip} (TTL: {ttl}s)")
    return ip

# Hàm flush cache
def flush_cache():
    cache.clear()
    print("Cache has been flushed.")

# Hiển thị cache hiện tại
def display_cache():
    print("\nCache contents:")
    for domain, (ip, expire) in cache.items():
        remaining = max(0, round(expire - time.time()))
        print(f" - {domain} → {ip} (TTL: {remaining}s)")
    print()

# Hiển thị thống kê
def show_stats():
    print(f"\nDNS Query Stats:")
    print(f" - Cache Hit: {stats['hit']}")
    print(f" - Cache Miss: {stats['miss']}\n")

# Menu dòng lệnh
def menu():
    while True:
        print("\n===== DNS Cache Simulator =====")
        print("1. Query domain")
        print("2. Show cache")
        print("3. Flush cache")
        print("4. Show stats")
        print("5. Exit")
        choice = input("→ Chọn chức năng (1-5): ")

        if choice == '1':
            domain = input("Nhập domain: ").strip()
            ttl = int(input("TTL (s): "))
            query(domain, ttl)
        elif choice == '2':
            display_cache()
        elif choice == '3':
            flush_cache()
        elif choice == '4':
            show_stats()
        elif choice == '5':
            print("Thoát chương trình.")
            break
        else:
            print("Lựa chọn không hợp lệ.")

# Khởi động chương trình
if __name__ == "__main__":
    menu()
