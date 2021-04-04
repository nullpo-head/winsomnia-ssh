#!/usr/bin/env python

import ctypes
import sys
import os
import argparse
import time
import subprocess

ES_SYSTEM_REQUIRED = 0x00000001
ES_DISPLAY_REQUIRED = 0x00000002
ES_AWAYMODE_REQUIRED = 0x00000040
ES_CONTINUOUS = 0x80000000


def main():
    parser = argparse.ArgumentParser("winsomnia")
    parser.add_argument("duration", type=int, nargs="?",
                        help="the duration in minutes to prevent Windows from sleeping.")
    parser.add_argument("-q", "--quiet",
                        action="store_true", help="don't output informational messages")
    args = parser.parse_args()

    if sys.platform not in ["win32", "cygwin"]:
        if not args.quiet:
            sys.stderr.write("Trying to run via python.exe\n")
        result = subprocess.run(["which", "python.exe"], capture_output=True)
        path = result.stdout.strip()
        if path == b"":
            sys.stderr.write("Error: python.exe is not in PATH\n")
            sys.exit(1)
        if path.endswith(b"WindowsApps\\python.exe"):
            sys.stderr.write(
                "Error: Your Python interpreter is installed via Windows Store. ")
            sys.stderr.write(
                "Windows Store app cannot be launched from WSL. Please install Python via the official installer.\n")

        result = subprocess.run(
            ["wslpath", "-w", __file__], capture_output=True)
        selfpath = result.stdout.strip().decode("utf-8")
        result = subprocess.run(["python.exe", selfpath] + sys.argv[1:])
        sys.exit(result.returncode)

    if not args.quiet:
        print("Kill this program by Ctrl+C to let Windows sleep")

    start = time.time()

    while True:
        if args.duration is not None and time.time() - start >= args.duration * 60:
            break
        err = ctypes.windll.kernel32.SetThreadExecutionState(
            ES_SYSTEM_REQUIRED | ES_CONTINUOUS)
        if err == 0:
            sys.stderr.write(
                "Error: Failed to call the API to prevent sleep\n")
        time.sleep(60)


if __name__ == "__main__":
    main()
