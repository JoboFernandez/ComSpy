import pickle
import sys
HEADER_LENGTH = 10
DISCONNECTION_MESSAGE = "!DISCONNECT"

def handle_unknown_message(role):
    if role == "client":
        print("[DISCONNECTED] Connection to the server has been severed.")
        sys.exit()
    elif role == "server":
        return False

def receive_message(socket, role="server"):
    try:
        msg_header = socket.recv(HEADER_LENGTH)
        if not len(msg_header):
            handle_unknown_message(role)
        msg_length = int(msg_header.decode("utf-8").strip())
        msg = pickle.loads(socket.recv(msg_length))
        return msg
    except:
        handle_unknown_message(role)