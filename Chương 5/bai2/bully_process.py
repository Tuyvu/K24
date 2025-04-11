import socket
import threading
import time
import sys

N = int(sys.argv[1])
MY_ID = int(sys.argv[2])
PORT_BASE = 6000
HOST = 'localhost'

is_leader = False
leader_id = None
alive = [True for _ in range(N)] 

lock = threading.Lock()

def log(msg):
    print(f"[P{MY_ID}] {msg}")

def send_message(dest_id, msg):
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.connect((HOST, PORT_BASE + dest_id))
            s.sendall(msg.encode())
    except:
        log(f"Không thể gửi đến P{dest_id} (có thể đã chết)")

def broadcast(msg):
    for i in range(N):
        if i != MY_ID:
            send_message(i, msg)

def start_election():
    global leader_id, is_leader
    log("==> Bắt đầu bầu cử")
    higher_ids = [i for i in range(MY_ID + 1, N)]
    responded = False

    for pid in higher_ids:
        send_message(pid, f"ELECTION {MY_ID}")

    # Đợi phản hồi
    def wait_for_response():
        nonlocal responded
        time.sleep(3)
        if not responded:
            become_leader()

    threading.Thread(target=wait_for_response).start()

    def become_leader():
        global is_leader, leader_id
        with lock:
            is_leader = True
            leader_id = MY_ID
            broadcast(f"COORDINATOR {MY_ID}")
            log("==> Tôi là LEADER mới")

def server_thread():
    global leader_id
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT_BASE + MY_ID))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            msg = conn.recv(1024).decode()
            if msg.startswith("ELECTION"):
                sender_id = int(msg.split()[1])
                log(f"Nhận ELECTION từ P{sender_id}")
                send_message(sender_id, f"OK {MY_ID}")
                start_election()
            elif msg.startswith("OK"):
                log(f"Nhận OK từ P{msg.split()[1]}")
            elif msg.startswith("COORDINATOR"):
                with lock:
                    leader_id = int(msg.split()[1])
                    log(f"==> P{leader_id} là LEADER mới")
                    if leader_id != MY_ID:
                        is_leader = False

def input_loop():
    global leader_id
    while True:
        cmd = input("Nhập 'e' để mô phỏng lỗi leader và khởi động bầu cử: ").strip()
        if cmd == 'e':
            with lock:
                if leader_id == MY_ID or leader_id is None:
                    log("Không có leader hoặc tôi là leader -> bỏ qua")
                else:
                    log(f"Phát hiện P{leader_id} đã chết")
                    start_election()

# Bắt đầu server và xử lý input
threading.Thread(target=server_thread, daemon=True).start()
time.sleep(1)
if MY_ID == N - 1:
    is_leader = True
    leader_id = MY_ID
    log("Tôi là LEADER ban đầu")
input_loop()
