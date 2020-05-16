""" Handle servers. """

import os

NAME = "name"
IP = "ip"
PORT = "port"
USER = "user"
RPATH = "remotepath"
LPATH = "mountpoint"


class SServer(object):
    """ Class that represents a server. """
    def __init__(self, name, details):
        self.details = details
        self.details[NAME] = name
        self.name = name

    def run(self, action):
        cmd = {"list":     "echo \"{NAME} {USER}@{IP}:{PORT} on {MOUNTPOINT}\"",
               "mount":    "mkdir -p {MOUNTPOINT} && sshfs -C -p {PORT} {USER}@{IP}:{RPATH} {MOUNTPOINT}",
               "unmount":  "fusermount -u {MOUNTPOINT}; rmdir {MOUNTPOINT}",
               "sftp":     "sftp -P{PORT} {USER}@{IP}:{RPATH}",
               "ssh":      "ssh -p {PORT} {USER}@{IP}"
               }[action]

        cmd = cmd.replace("{PORT}", self.details[PORT])   \
                 .replace("{USER}", self.details[USER])   \
                 .replace("{IP}", self.details[IP])       \
                 .replace("{RPATH}", self.details[RPATH]) \
                 .replace("{NAME}", self.details[NAME]) \
                 .replace("{MOUNTPOINT}", os.path.expanduser(self.details[LPATH]))

        os.system(cmd)
