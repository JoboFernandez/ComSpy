def get_menu():
    return {
        "main": {
            "s": "Spy computer server",
            "m": "Send message to the server",
            "!d": "Disconnect from the server"
        },
        "spy": {
            "!r": "Refresh screenshot list",
            "!b": "Back to main menu",
            "!d": "Disconnect from the server"
        },
        "chat": {
            "!b": "Back to main menu",
            "!d": "Disconnect from the server"
        }
    }

def print_menu(option):
    menu = get_menu()[option]
    for key, val in menu.items():
        print(f"{key} --> {val}")

def get_command_list():
    commands = []
    for key1, val1 in get_menu().items():
        for key2, val2 in val1.items():
            if key2 in commands:
                continue
            commands.append(key2)
    return commands