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
import logging
logging.basicConfig(filename='/home/pi/start_dashboards.log', encoding='utf-8', level=logging.DEBUG)


WAIT_BETWEEN_LAUNCHES_IN_SECONDS = os.environ.get("WAIT_BETWEEN_LAUNCHES_IN_SECONDS", 1)
NUM_OF_DESKTOPS = os.environ.get("NUM_OF_DESKTOPS", 9)


def launch_in_desktop(num: int):
    try:
        profile_name = f"Profile{num}"
        subprocess.Popen([
            "chromium-browser", "--start-fullscreen", "--start-maximized", "--noerrdialogs", f"--profile-directory={profile_name}", "https://dashboardv2.fabapps.io"
        ])
    except subprocess.CalledProcessError as e:
        logging.error(e)
        raise Exception(f"Make sure you have chrome and xdotool installed and "
                        f"{NUM_OF_DESKTOPS} workspaces and profiles configured") from e


def check_linux():
    if platform.system().lower() != "linux":
        raise Exception("This script is meant to run on Linux.")
    logging.debug("Linux OS found")


def main():
    logging.debug("Starting")
    try:
        check_linux()
    except Exception as e:
        logging.error(e)

    desktop_number = 1
    while True:
        logging.debug(f"Launching {desktop_number}")
        launch_in_desktop(desktop_number)
        desktop_number += 1
        if desktop_number > NUM_OF_DESKTOPS:
            break
        logging.debug(f"Waiting {WAIT_BETWEEN_LAUNCHES_IN_SECONDS} seconds before next run")
        time.sleep(WAIT_BETWEEN_LAUNCHES_IN_SECONDS)


if __name__ == "__main__":
    main()
