import socket
import threading
import os

# IP = "192.168.254.196"
IP = socket.gethostbyname(socket.gethostname())
PORT = 0
HEADER_LENGTH = 10
DISCONNECT_MESSAGE = "!DISCONNECT"
REQUEST_SCREENSHOT_LIST = "!REQUESTLIST"
SPY_MESSAGE = "!SPY"

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.listen()
print(f"[LISTENING] server is listening @ {IP}:{server_socket.getsockname()[1]}")

connections = [server_socket]
clients = {}

def receive_message(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_LENGTH) # bytes
        if not len(msg_header):
            return False
        msg_length = int(msg_header.decode("utf-8").strip()) # int
        msg = client_socket.recv(msg_length) # bytes
        return msg.decode("utf-8") # string
    except:
        return False

def handle_client(client_socket, hostname):
    while True:
        message = receive_message(client_socket)
        if message == DISCONNECT_MESSAGE or not message:
            break
        elif message == REQUEST_SCREENSHOT_LIST:
            screenshot_dir = os.path.join(os.getcwd(), "screenshot")
            os.chdir(screenshot_dir)
            print(os.listdir())
        # print(f"{clients[client_socket]}: {message}")

    client_socket.close()
    client_count = threading.activeCount() - 2
    print(f"[INFO] {hostname} has disconnected. "
          f"{client_count} {'spy' if client_count <= 1 else 'spies'} remaining.")

def start_server():
    while True:
        client_socket, client_address = server_socket.accept()
        hostname = receive_message(client_socket)
        clients[client_socket] = hostname

        thread = threading.Thread(target=handle_client, args=(client_socket, hostname))
        thread.start()
        client_count = threading.activeCount() - 1
        print(f"[NEW CONNECTION] {hostname} has connected. "
              f"A total of {client_count} client{'s are' if client_count > 1 else ' is'} spying.")

        message = f"[SPYING] You have penetrated the server.".encode("utf-8")
        message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
        client_socket.send(message_header + message)


if __name__ == "__main__":
    start_server()