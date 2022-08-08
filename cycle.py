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
import time
import logging
logging.basicConfig(filename='/home/pi/cycle.log', encoding='utf-8', level=logging.DEBUG)


WAIT_BETWEEN_SCREENS_IN_SECONDS = os.environ.get("WAIT_BETWEEN_SCREENS_IN_SECONDS", 10)


def check_linux():
    if platform.system().lower() != "linux":
        raise Exception("This script is meant to run on Linux.")
    logging.debug("Linux OS found")


def main():
    logging.debug("Starting")
    try:
        check_linux()
    except Exception as e:
        logging.debug(e)

    count = 0
    while True:
        logging.debug("Starting loop")
        all_browser_windows = subprocess.check_output("wmctrl -lGp | grep \"fab:apps\" | cut -d' ' -f1", shell=True).decode("utf-8").split("\n")
        all_browser_windows = list(filter(lambda x: x.strip(), all_browser_windows))
        num_browser_windows = len(all_browser_windows)
        logging.debug(f"Found {num_browser_windows} browser windows matching the pattern")

        count += 1

        logging.debug(f"count incremented to {count}")

        if count >= num_browser_windows:
            logging.debug("Reseting count")
            count = 0

        if len(all_browser_windows) and count < len(all_browser_windows):
            selected_browser_window = all_browser_windows[count]
            logging.debug(f"Selected browser window: {selected_browser_window}")
            subprocess.Popen(["wmctrl", "-i", "-a", selected_browser_window])

        logging.debug(f"Waiting {WAIT_BETWEEN_SCREENS_IN_SECONDS} seconds before next run")
        time.sleep(WAIT_BETWEEN_SCREENS_IN_SECONDS)


if __name__ == "__main__":
    main()
