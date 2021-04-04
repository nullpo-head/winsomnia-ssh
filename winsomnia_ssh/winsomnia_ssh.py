#!/usr/bin/env python

import argparse
import subprocess
import psutil
import sys
import os
import logging
import time
from typing import Optional

__version__ = "0.1.1"


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

    session = CurrentSshSession()
    if not session.is_ssh_session():
        logging.info("exiting because this is not a ssh session")
        sys.exit(0)

    # daemonize here because the shell that launched this process in its "~/.*rc" is waiting
    daemonize()
    # TODO: log to file if necessary

    logging.info("Detected winsomnia-ssh is running in a ssh session.")
    while session.is_alive():
        wait_completed_process_noblock()  # let zombie processes exit
        # Allow two processes to run at the same time for a minute
        # so that there is no time when there is not a single winsomnia process.
        run_winsomnia_noblock(3)
        time.sleep(120)


def check_prerequisite() -> Optional[str]:
    result = subprocess.run(["which", "python.exe"], capture_output=True)
    path = result.stdout.strip()
    if path == b"":
        return "python.exe is not in PATH.\n" \
               "Please Install Python for Windows via the official installer. " \
               "DO NOT install python for Windows via Microsoft Store due to a technical problem."
    result = subprocess.run(["which", "winsomnia"], capture_output=True)
    if path == "":
        return "winsomnia is not in PATH. Did you install winsomnia-ssh successfully?"
    return None


def daemonize():
    sys.stdin.close()
    sys.stderr.close()
    sys.stdout.close()
    sys.stdin = os.devnull
    null = open(os.devnull, "rw")
    sys.stdin = null
    sys.stderr = null
    sys.stdout = null
    if os.fork() == 0:
        return
    else:
        sys.exit(0)


def run_winsomnia_noblock(timeout: int):
    subprocess.Popen(["winsomnia", str(timeout), "-q"],
                     stdin=subprocess.DEVNULL)


def wait_completed_process_noblock():
    while True:
        try:
            if os.waitpid(0, os.WNOHANG) == (0, 0):
                break
        except ChildProcessError:
            # ignore no-child error
            break


class CurrentSshSession:
    def __init__(self):
        self.parents = psutil.Process().parents()
        self._is_ssh_session = None

    def is_ssh_session(self) -> bool:
        if self._is_ssh_session:
            return self._is_ssh_session
        self._is_ssh_session = any(
            filter(lambda p: p.name() == "sshd", self.parents))
        return self._is_ssh_session

    def is_alive(self) -> False:
        return self.is_ssh_session() and self.parents[0].is_running()


if __name__ == "__main__":
    main()
