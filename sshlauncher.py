#!/usr/bin/python

""" Quickly ssh/sftp/mount/unmount into another machine. """

import os
import sys
from configobj import ConfigObj

COMMANDS = {"list":     ("echo \"{NAME} {USER}@{IP}:{PORT} on {MOUNTPOINT}\"", "opt:apply_to_all"),
            "mount":    ("mkdir -p {MOUNTPOINT} && sshfs -C -p {PORT} {USER}@{IP}:{RPATH} {MOUNTPOINT}",),
            "unmount":  ("fusermount -u {MOUNTPOINT}; rmdir {MOUNTPOINT}",),
            "sftp":     ("sftp -P{PORT} {USER}@{IP}:{RPATH}",),
            "yafc":     ("yafc sftp://{USER}@{IP}:{PORT}/{RPATH}",),
            "ssh":      ("ssh -p {PORT} {USER}@{IP}",)
           }


def run_command(config, command_name, endpoint_name):
    """ Run a command on the specified endpoint. """

    NAME = "name"
    IP = "ip"
    PORT = "port"
    USER = "user"
    RPATH = "remotepath"
    LPATH = "mountpoint"

    endpoint_details = config[endpoint_name]
    cmd = COMMANDS[command_name][0] \
             .replace("{PORT}", endpoint_details[PORT])   \
             .replace("{USER}", endpoint_details[USER])   \
             .replace("{IP}", endpoint_details[IP])       \
             .replace("{RPATH}", endpoint_details[RPATH]) \
             .replace("{NAME}", endpoint_name) \
             .replace("{MOUNTPOINT}", os.path.expanduser(endpoint_details[LPATH]))

    os.system(cmd)


def command_applies_to_all(command_name):
    """
    Returns whether or not the command with the given name should
    be ran for all the endpoints in the configuration file (True)
    or only for the endpoints provided as parameter (False)
    """
    return "opt:apply_to_all" in COMMANDS[command_name]



if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: {} {list,mount,unmount,ssh,sftp} [ep1, ep2, ...]", sys.argv[0])
        sys.exit(1)

    (command_name, endpoints) = (sys.argv[1], sys.argv[2:])
    config = ConfigObj(os.path.expanduser('~/.remotes_config'))

    for ep in config:
        if ep in endpoints or command_applies_to_all(command_name):
            run_command(config, command_name, ep)
