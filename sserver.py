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

    def _replace_tokens(self, cmd):
        return cmd.replace("{PORT}", self.details[PORT])   \
                  .replace("{USER}", self.details[USER])   \
                  .replace("{IP}", self.details[IP])       \
                  .replace("{RPATH}", self.details[RPATH]) \
                  .replace("{NAME}", self.details[NAME]) \
                  .replace("{MOUNTPOINT}", os.path.expanduser(self.details[LPATH]))

    def echo(self):
        """ Return server info. Verbose. """
        command = self._replace_tokens("echo \"{NAME} {USER}@{IP}:{PORT} on {MOUNTPOINT}\"")
        os.system(command)

    def mount( self ):
        """ Mount the server. """
        command= self._replace_tokens("mkdir -p {MOUNTPOINT} && sshfs -C -p {PORT} {USER}@{IP}:{RPATH} {MOUNTPOINT}")
        os.system(command)

    def unmount( self ):
        """ Unmount the server. """
        command = self._replace_tokens("fusermount -u {MOUNTPOINT}; rmdir {MOUNTPOINT}")
        os.system(command)

    def sftp(self):
        """ SFTP into the server. """
        command = self._replace_tokens("sftp -P{PORT} {USER}@{IP}:{RPATH}")
        os.system(command)

    def ssh( self ):
        """ SSH into the server. """
        command = self._replace_tokens("ssh -p {PORT} {USER}@{IP}")
        os.system(command)
