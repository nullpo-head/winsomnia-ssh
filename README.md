# Winsomnia-Ssh

Winsomnia-Ssh prevents Windows from sleeping while your ssh session is active in WSL.

## Installation

```sh
pip install "git+https://github.com/nullpo-head/winsomnia-ssh"
```

## Usage

### Prevent sleep while your ssh session in WSL is active

Add the following line to your `~/.bashrc` or an equivalent file of your environment.

```sh
winsomnia-ssh &
```

As long as the shell session in WSL that launched `winsomnia-ssh` is active, it will prevent Windows from going to sleep.
It does nothing when your session is not in a ssh session, so you can just add the line above to your `.bashrc`.

Please note that the detection of ssh sessions assumes that your `sshd` is `sshd` of Linux (WSL2).
For your reference, here is an example tutorial of how to set up an ssh server in WSL2. [How to SSH into WSL2 on Windows 10 from an external machine - Scott Hanselman's Blog](https://www.hanselman.com/blog/how-to-ssh-into-wsl2-on-windows-10-from-an-external-machine).
The reference says that `DO NOT DO THE INSTRUCTIONS IN THIS POST` because it is simpler to use the native OpenSSH service of Windows, but `winsomnia-ssh` depends on Linux `sshd`, so please follow the instruction. Personally, I recommend you to set up a ssh server and port forwardings in WSL2 instead of Windows, because it is more flexible when you want to have more Linux services in the future.

### Manually prevent sleep for a while by CLI

`winsomnia-ssh` provides a handy CLI tool, `prevent-winsleep`.
`prevent-winsleep` allows you to prevent sleep whenever you want, regardless of whether you are in an ssh session or not.

```sh
prevent-winsleep [duration_in_minutes]
```

See `prevent-winsleep --help` for the detailed usage.
