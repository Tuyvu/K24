import time
import random

# 1. Root Server
root_server = {
    'com': '192.0.2.1',
    'org': '192.0.2.2',
    'vn': '192.0.2.3'
}

# 2. TLD Servers
tld_servers = {
    '192.0.2.1': {'example.com': '192.0.3.1', 'shop.com': '192.0.3.2'},
    '192.0.2.2': {'myorg.org': '192.0.3.3'},
    '192.0.2.3': {'gov.vn': '192.0.3.4'}
}

# 3. Authoritative Servers
auth_servers = {
    '192.0.3.1': {'www.example.com': '203.0.113.1', 'mail.example.com': '203.0.113.2'},
    '192.0.3.2': {'shop.com': '203.0.113.3'},
    '192.0.3.3': {'mail.myorg.org': '203.0.113.4', 'shop.myorg.org': '203.0.113.5'},
    '192.0.3.4': {'www.gov.vn': '203.0.113.6'}
}

# Giả lập timeout ngẫu nhiên
def simulate_timeout(probability=0.1):
    return random.random() < probability

# Phân giải tên
def resolve(domain):
    print(f"\nResolving domain: {domain}")
    parts = domain.split('.')
    if len(parts) < 2:
        print("Domain không hợp lệ.")
        return

    tld = parts[-1]
    domain2 = '.'.join(parts[-2:])

    # Step 1: Root
    print("\n[Step 1] Root Server:")
    start = time.time()
    if simulate_timeout():
        print("Root Server timeout!")
        return
    tld_server_ip = root_server.get(tld)
    if not tld_server_ip:
        print("TLD không được hỗ trợ.")
        return
    print(f"{tld} → {tld_server_ip} (TLD Server)")
    print(f"Time: {round(time.time() - start, 4)}s")

    # Step 2: TLD
    print("\n[Step 2] TLD Server:")
    start = time.time()
    if simulate_timeout():
        print("TLD Server timeout!")
        return
    domain_ip = tld_servers.get(tld_server_ip, {}).get(domain2)
    if not domain_ip:
        print("Không tìm thấy domain trong TLD Server.")
        return
    print(f"{domain2} → {domain_ip} (Authoritative Server)")
    print(f"Time: {round(time.time() - start, 4)}s")

    # Step 3: Authoritative
    print("\n[Step 3] Authoritative Server:")
    start = time.time()
    if simulate_timeout():
        print("Authoritative Server timeout!")
        return
    ip = auth_servers.get(domain_ip, {}).get(domain)
    if not ip:
        print("Không tìm thấy tên đầy đủ.")
        return
    print(f"{domain} → {ip}")
    print(f"Time: {round(time.time() - start, 4)}s")

# Thử nghiệm
test_domains = [
    "www.example.com",
    "mail.example.com",
    "shop.com",
    "mail.myorg.org",
    "shop.myorg.org",
    "www.gov.vn"
]

for domain in test_domains:
    resolve(domain)
