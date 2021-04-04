# Winsomnia-ssh and Winsomnia

`winsomnia-ssh` prevents Windows from going to sleep while your ssh session is active in WSL.
It also provides a simple CLI, `winsomnia`, which allows you to pause sleep whenever you want, for however long you want.

## Installation

Install `winsomnia-ssh` in WSL by `pip`.

```sh
pip install "git+https://github.com/nullpo-head/winsomnia-ssh"
```

`winsomnia-ssh` requires `python` both in WSL2 and Windows. Please install Python for Windows via [the official installer](https://www.python.org/downloads/). Please DO NOT install Python via Microsoft store. It appears that the store app cannot be launched from WSL.

If you install `winsomnia-ssh` in native Windows, `winsomnia` should work without problem.
`winsomnia-ssh` may be able to work, but it's not tested or supported.

## Usage

### Prevent sleep while your ssh session in WSL is active

Add the following line to your `~/.bashrc` or an equivalent file of your environment in WSL.

```sh
winsomnia-ssh &
```

As long as the shell session in WSL that launched `winsomnia-ssh` is active, it will prevent Windows from going to sleep.
It does nothing when your session is not in a ssh session, so you can just add the line above to your `.bashrc`.

Please note that the detection of ssh sessions assumes that your `sshd` is `sshd` of Linux (WSL).
For your reference, here is an example tutorial of how to set up an ssh server in WSL. [How to SSH into WSL2 on Windows 10 from an external machine - Scott Hanselman's Blog](https://www.hanselman.com/blog/how-to-ssh-into-wsl2-on-windows-10-from-an-external-machine).
Scott's article recommends that `DO NOT DO THE INSTRUCTIONS IN THIS POST` because it is simpler to use the native OpenSSH service of Windows. However, `winsomnia-ssh` depends on Linux `sshd`, so please follow the instruction. Personally, I recommend you to set up a ssh server and port forwardings in WSL2 instead of Windows, because it is more flexible when you want to have more Linux services in the future.

### Manually prevent sleep for a while by CLI

`winsomnia-ssh` provides a handy CLI tool, `winsomnia`.
`winsomnia` allows you to prevent sleep whenever you want, regardless of whether you are in an ssh session or not.

```sh
winsomnia [duration_in_minutes]
```

You can quit `winsomnia` to resume Windows Sleep.

```console
$ winsomnia
Trying to run via python.exe
Kill this program by Ctrl+C to let Windows sleep
^C
```

See `winsomnia --help` for the detailed usage.
