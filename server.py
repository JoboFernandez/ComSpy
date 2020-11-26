import socket

IP = "192.168.254.196"
PORT = 1234
HEADER_LENGTH = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen()

connections = [server_socket]
clients = {}

def receive_message(client_socket):
    msg_header = client_socket.recv(HEADER_LENGTH)

    if not msg_header:
        return False

    msg_length = int(msg_header.decode("utf-8").strip())
    msg = client_socket.recv(msg_length)

while True:
    for connection in connections:
        if connection == server_socket:
            client_socket, client_address = server_socket.accept()

