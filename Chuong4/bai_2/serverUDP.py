import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_socket.bind(("0.0.0.0", 12345))

clients = set()

print("UDP Server đang chạy...")

while True:
    message, addr = server_socket.recvfrom(1024)
    clients.add(addr)
    print(f"{addr}: {message.decode()}")

    # Gửi tin nhắn đến tất cả client
    for client in clients:
        if client != addr:
            server_socket.sendto(message, client)
