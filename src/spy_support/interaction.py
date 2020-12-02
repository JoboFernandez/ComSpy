import pickle
import sys

HEADER_LENGTH = 10
IMG_HEADER = 65526
CMD_REQUESTSCREENSHOTS = "!r"
CMD_VIEWIMAGE = "!v"
CMD_BACKTOMAIN = "!b"
CMD_DISCONNECT = "!d"
CMD_CHAT = "!c"

VIEW_IMAGE = "!v"

def disconnect_client(client_socket):
    send_message(client_socket, CMD_DISCONNECT)

def handle_unknown_message(role):
    if role == "client":
        print("[DISCONNECTED] Connection to the server has been severed.")
        sys.exit()
    elif role == "server":
        return False

def send_message(client_socket, msg):
    message = pickle.dumps(msg)
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(message_header + message)

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

def send_image(client_socket, image):
    image_header = f"{len(image):<{HEADER_LENGTH}}".encode("utf-8")
    client_socket.send(image_header + image)

def receive_image(client_socket):
    image_header = client_socket.recv(HEADER_LENGTH)
    image_length = int(image_header.decode("utf-8").strip())
    image = client_socket.recv(image_length)
    print("image_chunk length @ receive_message", len(image))
    return image

