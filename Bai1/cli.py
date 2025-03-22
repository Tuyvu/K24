import socket

# Thiết lập client
HOST = '127.0.0.1'  # Địa chỉ server (localhost)
PORT = 65432        # Cổng server đang lắng nghe

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((HOST, PORT))

message = "Xin chào, Server!"
client_socket.sendall(message.encode())

data = client_socket.recv(1024).decode()
print(f"Phản hồi từ server: {data}")

client_socket.close()
