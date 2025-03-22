import socket
import threading

# Danh sách client đang kết nối
clients = []

def broadcast(message, sender_socket):
    """Gửi tin nhắn đến tất cả các client trừ sender."""
    for client in clients:
        if client != sender_socket:
            try:
                client.send(message)
            except:
                clients.remove(client)

def handle_client(client_socket):
    """Nhận tin nhắn từ client và gửi đến các client khác."""
    while True:
        try:
            message = client_socket.recv(1024)
            if not message:
                break
            broadcast(message, client_socket)
        except:
            clients.remove(client_socket)
            break

def start_server():
    """Khởi động server và chấp nhận kết nối từ client."""
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.bind(("0.0.0.0", 12345))
    server_socket.listen(5)
    
    print("Server đang chạy...")

    while True:
        client_socket, addr = server_socket.accept()
        print(f"Client {addr} đã kết nối.")
        clients.append(client_socket)

        threading.Thread(target=handle_client, args=(client_socket,)).start()

start_server()
