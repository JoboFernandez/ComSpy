import socket

IP = "192.168.254.196"
PORT = 1234
HEADER_LENGTH = 10

def receive_message(client_socket):
    msg_header = client_socket.recv(HEADER_LENGTH)
    msg_length = int(msg_header.decode("utf-8").strip())
    msg = client_socket.recv(msg_length)
    return msg.decode("utf-8")

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.connect((IP, PORT))

hostname = socket.gethostname().encode("utf-8")
hostname_header = f"{len(hostname):<{HEADER_LENGTH}}".encode("utf-8")
client_socket.send(hostname_header + hostname)

while True:
    message = receive_message(client_socket)
    print(message)