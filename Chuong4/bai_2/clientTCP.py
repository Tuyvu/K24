import socket
import threading

def receive_messages(client_socket):
    """Nhận và hiển thị tin nhắn từ server."""
    while True:
        try:
            message = client_socket.recv(1024).decode("utf-8")
            print("\n" + message)
        except:
            print("Mất kết nối với server.")
            break

def start_client():
    """Kết nối đến server và gửi tin nhắn."""
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect(("127.0.0.1", 12345))

    threading.Thread(target=receive_messages, args=(client_socket,)).start()

    while True:
        message = input()
        client_socket.send(message.encode("utf-8"))

start_client()
