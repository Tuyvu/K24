import threading
import time
import random

class Process(threading.Thread):
    def __init__(self, pid, processes):
        super().__init__()
        self.pid = pid
        self.clock = 0
        self.processes = processes

    def log(self, action):
        print(f"[P{self.pid}] Clock = {self.clock} | {action}")

    def internal_event(self):
        self.clock += 1
        self.log("Internal Event")

    def send_message(self, receiver_pid):
        self.clock += 1
        self.log(f"Sending message to P{receiver_pid}")
        self.processes[receiver_pid].receive_message(self.pid, self.clock)

    def receive_message(self, sender_pid, timestamp):
        self.clock = max(self.clock, timestamp) + 1
        self.log(f"Received message from P{sender_pid} (timestamp={timestamp})")

    def run(self):
        for _ in range(5):  # Mỗi tiến trình thực hiện 5 hành động ngẫu nhiên
            action = random.choice(["internal", "send"])
            if action == "internal":
                self.internal_event()
            else:
                target = random.choice([p.pid for p in self.processes if p.pid != self.pid])
                self.send_message(target)
            time.sleep(random.uniform(0.5, 1.5))  # Giả lập độ trễ

def simulate_lamport_clock(N=3):
    processes = [Process(i, None) for i in range(N)]
    for p in processes:
        p.processes = processes
    for p in processes:
        p.start()
    for p in processes:
        p.join()

simulate_lamport_clock(N=3)
