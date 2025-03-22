import socket
import threading

server_address = ("127.0.0.1", 12345)
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

def receive_messages():
    """Nhận tin nhắn từ server."""
    while True:
        message, _ = client_socket.recvfrom(1024)
        print("\n" + message.decode())

threading.Thread(target=receive_messages, daemon=True).start()

while True:
    message = input()
    client_socket.sendto(message.encode(), server_address)
