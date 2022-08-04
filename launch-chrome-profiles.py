#!/usr/bin/env python3

"""
Launch Chrome profiles in different workspaces

This script assumes that:
- you have xdotool* installed
- you have installed Chromium** web browser
- you have NUM_OF_DESKTOPS chrome profiles setup
- you have set up NUM_OF_DESKTOPS workspaces

* sudo apt update && sudo apt install -y xdotool
** installed by default on raspbian
"""

import os
import platform
import subprocess
from tabnanny import check
import time


WAIT_BETWEEN_SCREENS_IN_SECONDS = os.environ.get("WAIT_BETWEEN_SCREENS_IN_SECONDS", 5)
NUM_OF_DESKTOPS = os.environ.get("NUM_OF_DESKTOPS", 9)


def change_num_desktops(num):
    try:
        subprocess.check_call(["xdotool", "set_num_desktops", str(num)])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Make sure you have xdotool installed and {NUM_OF_DESKTOPS} "
                        f"workspaces configured") from e


def launch_in_desktop(num: int):
    try:
        profile_name = f"Profile {num}"
        subprocess.check_call(["xdotool", "set_desktop", str(num)])
        subprocess.Popen([
            "chromium", "--start-fullscreen", f"--profile-directory='{profile_name}'"
        ])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Make sure you have chrome and xdotool installed and "
                        f"{NUM_OF_DESKTOPS} workspaces and profiles configured") from e


def check_linux():
    if platform.system().lower() != "linux":
        raise Exception("This script is meant to run on Linux.")


def main():
    check_linux()
    change_num_desktops(NUM_OF_DESKTOPS)

    desktop_number = 1
    while True:
        print(f"Launching {desktop_number}")
        launch_in_desktop(desktop_number)
        desktop_number += 1
        if desktop_number > NUM_OF_DESKTOPS:
            break
        time.sleep(WAIT_BETWEEN_SCREENS_IN_SECONDS)


if __name__ == "__main__":
    main()
