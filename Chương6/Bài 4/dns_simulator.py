import time
import random

class NameServer:
    def __init__(self, name, records=None, delegates=None):
        self.name = name
        self.records = records or {}  # tên miền → IP
        self.delegates = delegates or {}  # vùng con → NameServer
        self.cache = {}  # cache nội bộ

    def resolve(self, domain_parts, timeout=2):
        domain_str = ".".join(domain_parts)

        # Check cache
        if domain_str in self.cache:
            print(f"[{self.name}] Cache hit for {domain_str}")
            return self.cache[domain_str]

        # Nếu là domain trực tiếp
        if len(domain_parts) == 1 and domain_parts[0] in self.records:
            ip = self.records[domain_parts[0]]
            self.cache[domain_str] = ip
            print(f"[{self.name}] Found IP for {domain_str} → {ip}")
            return ip

        # Nếu có delegate phù hợp
        if domain_parts[-1] in self.delegates:
            next_server = self.delegates[domain_parts[-1]]
            try:
                time.sleep(random.uniform(0.1, timeout))  # mô phỏng độ trễ
                return next_server.resolve(domain_parts[:-1])
            except TimeoutError:
                print(f"[{self.name}] Timeout khi gọi {next_server.name}")
                return None

        print(f"[{self.name}] Không tìm thấy {domain_str}")
        return None
