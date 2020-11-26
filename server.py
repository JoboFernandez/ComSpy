import socket

IP = "192.168.254.196"
PORT = 1234
HEADER_LENGTH = 10

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((IP, PORT))
server_socket.listen()
print(f"[LISTENING] server is listening")

connections = [server_socket]
clients = {}

def receive_message(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_LENGTH)
        if not len(msg_header):
            return False
        msg_length = int(msg_header.decode("utf-8").strip())
        msg = client_socket.recv(msg_length)
        return msg.decode("utf-8")
    except:
        return False

while True:
    client_socket, client_address = server_socket.accept()
    hostname = receive_message(client_socket)
    if not hostname:
        continue
    clients[client_socket] = hostname
    print(f"{client_address[0]}:{client_address[1]} >> {hostname}")
    while True:
        for connection in connections:
            if connection != server_socket:
                message = "WELCOME TO DESKTOP-SPY PROGRAM".encode("utf-8")
                message_header = f"{len(message)}:<{HEADER_LENGTH}".encode("utf-8")
                connection.send(message_header + message)