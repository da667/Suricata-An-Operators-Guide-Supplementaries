# Purpose of this file:
For Windows and Linux, enabling the SSLKEYLOGFILE env variable to log TLS master secrets is kinda straightfoward. But for macOS, its a bit of a slog. So in this directory, I have two files:
- `keylogfile-la.plist`
- `keylogfile-ld.plist`

For readers/users of *Suricata:An Operator's guide*, who want to be able to automatically log TLS master secrets (for applications/libraries that actually support it), for all applications launched from the GUI, you need to use a plist. Because macOS is *almost* but not really UNIX-like, the methods that work on most Linux distros (laid out in chapter 10), don't work here.

**The guidance in this file is ONLY for macOS users who insist on using the plist method for defining the SSLKEYLOGFILE environment variable**. If you're content with defining the environment variable in `/etc/zprofile`, `~/.zprofile` for `zsh`, or `/etc/profile`, `~/.profile` for `bash`, and launching applications from your terminal session so that they inherit the variable, you don't need to do any of this.

## Plist Files:
- `keylogfile-la.plist`: This is a plist meant to run in a local user's `/Users/[username]/Library/LaunchAgents` directory. To use this file, you will need to run:
  - `mkdir /User/[username]/LaunchAgents`
  - `mv keylogfile-la.plist /Users/[username]/Library/LaunchAgents`
  - `touch /Users/[username]/.keylogfile.txt`
  - `launchctl load /Users/[username]/Library/LaunchAgents/keylogfile-la.plist`

Note: in all of the commands above, you will need to replace the text `[user]` with the name of user account you want to apply the SSLKEYLOGFILE environment variable for. **It is very highly recommended that you are currently logged in as the user you wish to configure TLS master secrets logging for, to ensure that the files and directories in question all have the correct file permissions. It is also very important that the user have write access to the file specified in the SSLKEYLOGFILE variable, or else macOS will not do anything at all.** Finally, the keylog file should automatically rotate each time the user logs in. The keylog file will be placed in the user's home directory, as a hidden file with the filename that looks like this: `.keylogfile-[username]-YY-mm-dd.txt`
- `keylogfile-ld.plist`: This is a plist file that is meant to run in `/Library/LaunchDaemons`. Adding this file to that directory should, in practice, apply the SSLKEYLOGFILE environment variable to all users. Adding this plist file to that directory will require `root` permissions to do so. Here are the commands you'll need to run:
  - `sudo cp keylogfile-ld.plist /Library/LaunchDaemons`
  - `sudo launchctl load /Libary/Launchdaemons/keylogfile-ld.plist`

Note: by default, the `keylogfile-ld.plist` will write to `/tmp/.keylogfile.txt`, which is one of the few places where every user on macOS has write access. But, as is customary on unix systems, the tmp directory is, well, *temporary*. So, either you will need to:
- Find a way to regularly rotate out the `.keylogfile.txt` out of /tmp into some sort of an archive
- Create a directory in which everyone has write access to the file, and in so doing, perhaps modify the filename to include some sort of a timestamp and/or maybe individual usernames so that you don't have one GIANT TLS master secrets file.
