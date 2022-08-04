#!/usr/bin/env python3

"""
Cycle between different workspaces automatically.

This script assumes that:
- you have xdotool installed (sudo apt update && sudo apt install -y xdotool)
- you have set up NUM_OF_DESKTOPS workspaces
"""

import os
import platform
import subprocess
from tabnanny import check
import time


WAIT_BETWEEN_SCREENS_IN_SECONDS = os.environ.get("WAIT_BETWEEN_SCREENS_IN_SECONDS", 30)
NUM_OF_DESKTOPS = os.environ.get("NUM_OF_DESKTOPS", 9)


def change_num_desktops(num):
    try:
        subprocess.check_call(["xdotool", "set_num_desktops", str(num)])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Make sure you have xdotool installed and {NUM_OF_DESKTOPS} "
                        f"workspaces configured") from e


def change_desktop(num: int):
    try:
        subprocess.check_call(["xdotool", "set_desktop", str(num)])
    except subprocess.CalledProcessError as e:
        raise Exception(f"Make sure you have xdotool installed and {NUM_OF_DESKTOPS} "
                        f"workspaces configured") from e


def check_linux():
    if platform.system().lower() != "linux":
        raise Exception("This script is meant to run on Linux.")


def main():
    check_linux()
    change_num_desktops(NUM_OF_DESKTOPS)

    desktop_number = 1
    while True:
        change_desktop(desktop_number)
        desktop_number += 1
        if desktop_number > NUM_OF_DESKTOPS:
            desktop_number = 1
        time.sleep(WAIT_BETWEEN_SCREENS_IN_SECONDS)


if __name__ == "__main__":
    main()
