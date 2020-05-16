""" Handle servers. """

import os

IP = "ip"
PORT = "port"
USER = "user"
RPATH = "remotepath"
LPATH = "mountpoint"


class SServer(object):
    """ Class that represents a server. """
    def __init__(self, name, details):
        self.details = details
        self.name = name

    def is_mounted(self):
        return os.path.ismount(os.path.expanduser(self.details[LPATH]))

    @property
    def str_short(self):
        """ Return server info. Summary. """
        symbol = " [*]" if self.is_mounted() else " [ ]"
        return "%s %s" % (symbol, self.name)

    @property
    def str_long(self):
        """ Return server info. Verbose. """
        return "%s --- %s@%s:%s on %s" % (self.str_short,
                                          self.details[USER],
                                          self.details[IP],
                                          self.details[PORT],
                                          self.details[LPATH])

    def _replace_tokens(self, cmd):
        return cmd.replace("{PORT}", self.details[PORT])   \
                  .replace("{USER}", self.details[USER])   \
                  .replace("{IP}", self.details[IP])       \
                  .replace("{RPATH}", self.details[RPATH]) \
                  .replace("{MOUNTPOINT}", os.path.expanduser(self.details[LPATH]))

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
