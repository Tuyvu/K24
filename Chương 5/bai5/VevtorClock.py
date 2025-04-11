import threading
import time
import random
import copy

class Process(threading.Thread):
    def __init__(self, pid, n, processes):
        super().__init__()
        self.pid = pid
        self.n = n
        self.vclock = [0] * n
        self.processes = processes

    def log(self, action):
        print(f"[P{self.pid}] VC = {self.vclock} | {action}")

    def internal_event(self):
        self.vclock[self.pid] += 1
        self.log("Internal Event")

    def send_message(self, receiver_pid):
        self.vclock[self.pid] += 1
        self.log(f"Sending message to P{receiver_pid}")
        # Send a copy to simulate message transmission
        self.processes[receiver_pid].receive_message(self.pid, copy.deepcopy(self.vclock))

    def receive_message(self, sender_pid, incoming_vc):
        for i in range(self.n):
            self.vclock[i] = max(self.vclock[i], incoming_vc[i])
        self.vclock[self.pid] += 1
        self.log(f"Received message from P{sender_pid} with VC={incoming_vc}")

    def run(self):
        for _ in range(5):  # thực hiện 5 hành động
            action = random.choice(["internal", "send"])
            if action == "internal":
                self.internal_event()
            else:
                targets = [p.pid for p in self.processes if p.pid != self.pid]
                target = random.choice(targets)
                self.send_message(target)
            time.sleep(random.uniform(0.5, 1.5))  # giả lập độ trễ

def simulate_vector_clock(N=3):
    processes = [Process(i, N, None) for i in range(N)]
    for p in processes:
        p.processes = processes
    for p in processes:
        p.start()
    for p in processes:
        p.join()

simulate_vector_clock(N=3)
