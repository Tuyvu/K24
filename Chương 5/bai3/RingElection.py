import threading
import time
import random

class Process(threading.Thread):
    def __init__(self, pid, processes):
        super().__init__()
        self.pid = pid
        self.processes = processes
        self.alive = True
        self.is_leader = False

    def run(self):
        while self.alive:
            time.sleep(1)

    def receive_election(self, msg, initiator):
        if not self.alive:
            return
        msg.append(self.pid)
        next_pid = (self.pid + 1) % len(self.processes)

        while not self.processes[next_pid].alive:
            next_pid = (next_pid + 1) % len(self.processes)

        print(f"[P{self.pid}] chuyển thông điệp: {msg}")
        if next_pid == initiator:
            # Vòng lặp kết thúc, chọn leader
            new_leader = max(msg)
            print(f"[P{self.pid}] ==> Leader mới là P{new_leader}")
            self.processes[new_leader].announce_leader()
        else:
            self.processes[next_pid].receive_election(msg, initiator)

    def announce_leader(self):
        for p in self.processes:
            if p.alive:
                p.is_leader = (p.pid == self.pid)
        print(f"[P{self.pid}] phát COORDINATOR → Tôi là leader!")

def simulate_ring_election(N, fail_leader=True):
    processes = [Process(i, None) for i in range(N)]
    for p in processes:
        p.processes = processes
        p.start()

    leader = max(processes, key=lambda x: x.pid)
    leader.is_leader = True
    print(f"[System] Ban đầu P{leader.pid} là leader")

    if fail_leader:
        print(f"[System] Mô phỏng leader P{leader.pid} bị lỗi")
        leader.alive = False

    time.sleep(2)

    # Chọn tiến trình bất kỳ còn sống để bắt đầu bầu cử
    starter = random.choice([p for p in processes if p.alive])
    print(f"[System] P{starter.pid} khởi động bầu cử")
    starter.receive_election([starter.pid], starter.pid)

simulate_ring_election(N=5, fail_leader=True)
