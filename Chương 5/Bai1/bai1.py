import socket
import threading
import time
import sys

N = int(sys.argv[1])
MY_ID = int(sys.argv[2])
PORT_BASE = 5000
HOST = 'localhost'

lock = threading.Lock()
timestamp = 0
requesting = False
reply_count = 0
deferred = set()
request_time = None

def log(msg):
    print(f"[P{MY_ID}] {msg}")

def send_message(dest_id, msg):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((HOST, PORT_BASE + dest_id))
        s.sendall(msg.encode())

def broadcast(msg):
    for i in range(N):
        if i != MY_ID:
            send_message(i, msg)

def enter_critical_section():
    global timestamp, request_time, requesting, reply_count, deferred
    with lock:
        requesting = True
        timestamp += 1
        request_time = timestamp
        reply_count = 0
        deferred = set()
        log(f"Requesting CS at time {timestamp}")
    broadcast(f"REQUEST {MY_ID} {request_time}")

def exit_critical_section():
    with lock:
        requesting = False
        log("Exiting CS")
        for pid in deferred:
            send_message(pid, f"REPLY {MY_ID}")
            log(f"Sent REPLY to {pid}")
        deferred.clear()

def server_thread():
    global timestamp, reply_count, deferred
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT_BASE + MY_ID))
    s.listen()

    while True:
        conn, addr = s.accept()
        with conn:
            data = conn.recv(1024).decode()
            if data.startswith("REQUEST"):
                sender, their_time = map(int, data.split()[1:])
                with lock:
                    timestamp = max(timestamp, their_time) + 1
                    if (not requesting or 
                        (their_time, sender) < (request_time, MY_ID)):
                        send_message(sender, f"REPLY {MY_ID}")
                        log(f"REPLY sent to {sender}")
                    else:
                        deferred.add(sender)
                        log(f"Deferred REPLY to {sender}")

            elif data.startswith("REPLY"):
                with lock:
                    reply_count += 1
                    log(f"REPLY received ({reply_count}/{N-1})")
                    if reply_count == N - 1:
                        log("==> Entering CS")
                        time.sleep(2) 
                        exit_critical_section()

def input_loop():
    while True:
        inp = input("Nhấn ENTER để yêu cầu CS...")
        enter_critical_section()

threading.Thread(target=server_thread, daemon=True).start()
input_loop()
