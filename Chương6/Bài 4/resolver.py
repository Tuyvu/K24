import time

class NameServer:
    def __init__(self, name, records=None, delegates=None, ttl=30):
        self.name = name
        self.records = records or {}  # domain -> (IP, expiry_time)
        self.delegates = delegates or {}  # subdomain -> NameServer
        self.cache = {}  # domain -> (IP, expiry_time)
        self.ttl = ttl

    def resolve(self, domain):
        print(f"[{self.name}] Resolving {domain}")

        if domain in self.cache:
            ip, expiry = self.cache[domain]
            if expiry >= time.time():
                print(f"[{self.name}] Cache HIT for {domain}")
                return ip
            else:
                print(f"[{self.name}] Cache EXPIRED for {domain}")
                del self.cache[domain]

        if domain in self.records:
            ip = self.records[domain]
            expiry = time.time() + self.ttl
            self.cache[domain] = (ip, expiry)
            return ip

        for sub, delegate in self.delegates.items():
            if domain.endswith(sub):
                return delegate.resolve(domain)

        print(f"[{self.name}] {domain} NOT FOUND")
        return None

    def flush_cache(self):
        self.cache.clear()

    def print_cache(self):
        print(f"[{self.name}] Current cache:")
        for domain, (ip, expiry) in self.cache.items():
            print(f"  {domain} => {ip}, expires at {time.ctime(expiry)}")
