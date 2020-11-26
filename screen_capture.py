'''
SCREEN CAPTURE
1. This program creates a folder where screenshots are stored
2. Screenshots are captured are certain time interval and are stored in the screenshot folder
3. A file capacity variable is used to limit the quantity of captured images and save disk space
4. At file capacity, old files are replaced by new ones
'''

from datetime import datetime
import pyautogui
import time
import shutil
import os
import sys


def start_screen_capture():
    screenshot_dir = os.path.join(os.getcwd(), "screenshot")
    if not(os.path.isdir(screenshot_dir)):
        if os.path.exists(screenshot_dir):
            print(f"[!] An unknown document named screenshot exists in {os.getcwd()}. Either rename or remove this file.")
            sys.exit()
    else:
        shutil.rmtree(screenshot_dir)
    os.mkdir(screenshot_dir)
    os.chdir(screenshot_dir)

    file_capacity = 4
    capture_time_interval = 5
    file_holder = []
    while True:
        if len(os.listdir()) == file_capacity:
            os.remove(file_holder.pop(0))
        timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
        filename = f"desktopspy_{timestamp}.png"
        pyautogui.screenshot().save(fr"{filename}")
        file_holder.append(filename)
        time.sleep(capture_time_interval)


if __name__ == "__main__":
    print("[RUNNING] program is running")
    start_screen_capture()
