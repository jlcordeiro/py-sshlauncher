#!/usr/bin/python

""" Quickly ssh/sftp/mount/unmount into another machine. """

import os
import sys
from configobj import ConfigObj

COMMANDS = {"list":     "echo \"{NAME} {USER}@{IP}:{PORT} on {MOUNTPOINT}\"",
            "mount":    "mkdir -p {MOUNTPOINT} && sshfs -C -p {PORT} {USER}@{IP}:{RPATH} {MOUNTPOINT}",
            "unmount":  "fusermount -u {MOUNTPOINT}; rmdir {MOUNTPOINT}",
            "sftp":     "sftp -P{PORT} {USER}@{IP}:{RPATH}",
            "ssh":      "ssh -p {PORT} {USER}@{IP}"
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
        cmd = COMMANDS[action] \
                 .replace("{PORT}", self.details[self.PORT])   \
                 .replace("{USER}", self.details[self.USER])   \
                 .replace("{IP}", self.details[self.IP])       \
                 .replace("{RPATH}", self.details[self.RPATH]) \
                 .replace("{NAME}", self.name) \
                 .replace("{MOUNTPOINT}", os.path.expanduser(self.details[self.LPATH]))

        os.system(cmd)


def run(command_name, server_names):
    CONFIG = ConfigObj(os.path.expanduser('~/.remotes_config'))
    servers = [Endpoint(cname, CONFIG[cname])
                for cname in CONFIG
                if cname in server_names or command_name == "list"]
    servers.sort(key=lambda s: s.name)

    if servers is None or len(servers) < 1:
        print("Server not found.")
        return -1

    for s in servers:
        s.run(command_name)

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: {} {list,mount,unmount,ssh,sftp} [ep1, ep2, ...]", sys.argv[0])
        sys.exit(1)

    (command, endpoints) = (sys.argv[1], sys.argv[2:])
    run(command, endpoints)
