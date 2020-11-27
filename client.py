import socket
import sys

IP = "192.168.254.196"
HEADER_LENGTH = 10
DISCONNECT_MESSAGE = "!DISCONNECT"
REQUEST_SCREENSHOT_LIST = "!REQUESTLIST"
SPY_MESSAGE = "!SPY"

def receive_message(client_socket):
    try:
        msg_header = client_socket.recv(HEADER_LENGTH) # bytes
        if not len(msg_header):
            print("[DISCONNECT] Connection to the server has been severed.")
            sys.exit()
        msg_length = int(msg_header.decode("utf-8").strip()) # int
        msg = client_socket.recv(msg_length) # bytes
        return msg.decode("utf-8") # string
    except:
        print("[DISCONNECT] Connection to the server has been severed.")
        sys.exit()

def send_message(client_socket, msg):
    message = msg.encode("utf-8") # bytes
    message_header = f"{len(message):<{HEADER_LENGTH}}".encode("utf-8") # bytes
    client_socket.send(message_header + message)

def send_message_request(client_socket):
    print_submenu()

    while True:
        message = input("Your command/message: ")
        if message.lower() == "!b":
            break
        elif message.lower() == "!x":
            send_message(client_socket, DISCONNECT_MESSAGE)
            sys.exit()
        else:
            send_message(client_socket, message)

def spy_server(client_socket):
    print_submenu()

    while True:
        message = input("Your command/message: ")
        if message.lower() == "!b":
            break
        elif message.lower() == "!x":
            send_message(client_socket, DISCONNECT_MESSAGE)
            sys.exit()
        else:
            send_message(client_socket, message)

def get_menu():
     return {
        "s": "Spy computer server",
        "m": "Send message to the server",
        "!x": "Disconnect from the server"
    }

def print_submenu():
    submenu = {
        "!b": "Back to main menu",
        "!x": "Disconnect from the server"
    }
    print("Menu:")
    for key, val in submenu:
        print(f"{key} --> {val}")

def start_client():
    valid = False
    while not valid:
        port_temp = input("Enter server port number: ")
        if port_temp.isnumeric():
            port = int(port_temp)
            valid = True
        else:
            print("[!] Invalid input")

    client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    client_socket.connect((IP, port))

    send_message(client_socket, socket.gethostname())
    welcome_message = receive_message(client_socket)
    print(f"\n{welcome_message}\n")

    while True:
        print("\nPlease select a command of your choice from the menu below")
        print("Menu: ")
        for key, val in get_menu().items():
            print(f"{key} --> {val}")

        valid = False
        while not valid:
            command = input("Your command: ")
            if command.lower() in get_menu().keys():
                command = command.lower()
                valid = True
            else:
                print("[!] Command not recognized.")

        if command == "s":
            send_message(client_socket, REQUEST_SCREENSHOT_LIST)
            spy_server(client_socket)
        elif command == "m":
            send_message_request(client_socket)
        elif command == "!x":
            send_message(client_socket, DISCONNECT_MESSAGE)
            sys.exit()


if __name__ == "__main__":
    start_client()