#!/usr/bin/env python

import argparse
import subprocess
import psutil
import sys
import logging
import time
from typing import Optional

__version__ = "0.1.0"


def main():
    parser = argparse.ArgumentParser("winsomnia-ssh")
    parser.add_argument("--version", action="version",
                        version="%(prog)s {version}".format(version=__version__))
    parser.add_argument("-v", "--verbose", action="store_true",
                        help="Show verbose logging")
    args = parser.parse_args()
    if args.verbose:
        logging.basicConfig(level=logging.DEBUG)

    err = check_prerequisite()
    if err:
        logging.critical(err)
        sys.exit(1)

    if not is_ssh_session():
        logging.info("exiting because this is not a ssh session")
        sys.exit(0)
    logging.info("Detected winsomnia-ssh is running in a ssh session.")

    logging.info("Keep Windows awake")
    parent = psutil.Process().parent()
    while parent.is_running():
        if not prevent_winsleep(3):
            logging.critical("prevent-winsleep failed")
            sys.exit(1)
        time.sleep(120)


def check_prerequisite() -> Optional[str]:
    result = subprocess.run(["which", "python.exe"], capture_output=True)
    path = result.stdout.strip()
    if path == b"":
        return "python.exe is not in PATH.\n" \
               "Please Install Python for Windows via the official installer. " \
               "DO NOT install python for Windows via Microsoft Store due to a technical problem."
    result = subprocess.run(["which", "prevent-winsleep"], capture_output=True)
    if path == "":
        return "prevent-winsleep is not in PATH. Did you install insomni-ssh successfully?"
    return None


def is_ssh_session() -> bool:
    return any(filter(lambda p: p.name() == "sshd", psutil.Process().parents()))


def prevent_winsleep(timeout: int) -> bool:
    result = subprocess.run(["prevent-winsleep", str(timeout), "-q"])
    return result.returncode == 0


if __name__ == "__main__":
    main()
