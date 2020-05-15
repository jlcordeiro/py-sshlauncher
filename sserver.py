""" Handle servers. """

import os
from configobj import ConfigObj

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
        symbol = " [*]" if self.is_mounted() is True else " [ ]"
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
                  .replace("{MOUNTPOINT}", self.details[LPATH])

    def mount( self ):
        """ Mount the server. """
        if not self.is_mounted():
            mdir = os.path.expanduser(self.details[LPATH])
            if os.path.isdir(mdir) is False:
                os.mkdir(mdir)

            try:
                command= self._replace_tokens("sshfs -C -p {PORT} {USER}@{IP}:{RPATH} {MOUNTPOINT}")
                os.system(command)
            except:
                # if mounting fails for some reason, make sure mtab is clean
                # mark the server as mounted anyway to begin with,
                # so that unmount runs
                if res is not True:
                    self.unmount()

    def unmount( self ):
        """ Unmount the server. """
        if self.is_mounted():
            mdir = os.path.expanduser(self.details[LPATH])

            try:
                command = self._replace_tokens("fusermount -u {MOUNTPOINT}")
                os.system(command)

                try:
                    os.rmdir(mdir)
                except OSError:
                    pass
            except OSError as uex:
                print(uex)

    def sftp(self):
        """ SFTP into the server. """
        command = self._replace_tokens("sftp -P{PORT} {USER}@{IP}:{RPATH}")
        os.system(command)


    def ssh( self ):
        """ SSH into the server. """
        command = self._replace_tokens("ssh -p {PORT} {USER}@{IP}")
        os.system(command)

def valid_server(server, wanted_state):
    """ Tells whether or not a server is in the wanted state. The possible
        values for wanted_state are ('any', 'mounted', 'unmounted') """

    return (wanted_state == 'any') or \
           (wanted_state == 'mounted' and server.mounted) or \
           (wanted_state == 'unmounted' and not server.mounted)

class SServerList(object):
    """ List of servers. """

    def __init__(self, filename):
        """ Constructor. Appends all servers found on the configuration file
            to the local list of servers. """

        final_path = os.path.expanduser(filename)
        config = ConfigObj(final_path)

        self.servers = [SServer(cname, config[cname]) for cname in config]
        self.servers.sort(key=lambda s: s.name)

    def find_all_containing(self, name):
        """ Get the servers that have a name matching the provided term. """
        return [ s for s in self.servers if name in s.name ]

    def find(self, name):
        """ Get the first server that has a name matching the provided name. """
        return [ s for s in self.servers if name == s.name ][:1]
