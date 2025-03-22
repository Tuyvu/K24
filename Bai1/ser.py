import socket

# Thiết lập server
HOST = '127.0.0.1'  # Địa chỉ localhost
PORT = 65432        # Cổng cố định

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(1)  # Lắng nghe tối đa 1 client

print(f"Server đang lắng nghe trên {HOST}:{PORT}...")

while True:
    conn, addr = server_socket.accept()
    print(f"Kết nối từ {addr}")

    data = conn.recv(1024).decode()
    if not data:
        break

    print(f"Nhận từ client: {data}")
    conn.sendall(f"Server nhận được: {data}".encode())

    conn.close()
