#!/usr/bin/python

""" Quickly ssh/sftp/mount/unmount into another machine. """

import os
import sys
from configobj import ConfigObj

COMMANDS = {"list":     ("echo \"{NAME} {USER}@{IP}:{PORT} on {MOUNTPOINT}\"", "opt:apply_to_all"),
            "mount":    ("mkdir -p {MOUNTPOINT} && sshfs -C -p {PORT} {USER}@{IP}:{RPATH} {MOUNTPOINT}",),
            "unmount":  ("fusermount -u {MOUNTPOINT}; rmdir {MOUNTPOINT}",),
            "sftp":     ("sftp -P{PORT} {USER}@{IP}:{RPATH}",),
            "ssh":      ("ssh -p {PORT} {USER}@{IP}",)
           }

class Endpoint(object):
    NAME = "name"
    IP = "ip"
    PORT = "port"
    USER = "user"
    RPATH = "remotepath"
    LPATH = "mountpoint"

    """ Class that represents a server. """
    def __init__(self, name, details):
        self.details = details
        self.name = name

    def run(self, action):
        cmd = COMMANDS[action][0] \
                 .replace("{PORT}", self.details[self.PORT])   \
                 .replace("{USER}", self.details[self.USER])   \
                 .replace("{IP}", self.details[self.IP])       \
                 .replace("{RPATH}", self.details[self.RPATH]) \
                 .replace("{NAME}", self.name) \
                 .replace("{MOUNTPOINT}", os.path.expanduser(self.details[self.LPATH]))

        os.system(cmd)

def command_applies_to_all(command_name):
    """
    Returns whether or not the command with the given name should
    be ran for all the endpoints in the configuration file (True)
    or only for the endpoints provided as parameter (False)
    """
    return "opt:apply_to_all" in COMMANDS[command_name]

def run(command_name, server_names):
    CONFIG = ConfigObj(os.path.expanduser('~/.remotes_config'))

    # if a command that should apply to all endpoints
    if command_applies_to_all(command_name):
        server_names.sort()
        for ep in CONFIG:
            Endpoint(ep, CONFIG[ep]).run(command_name)
        return

    
    for ep in server_names:
        if ep in CONFIG:
            Endpoint(ep, CONFIG[ep]).run(command_name)
        else:
            print("Endpoint {} not found in config.", ep)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: {} {list,mount,unmount,ssh,sftp} [ep1, ep2, ...]", sys.argv[0])
        sys.exit(1)

    (command, endpoints) = (sys.argv[1], sys.argv[2:])
    run(command, endpoints)
