import os
from configobj import ConfigObj
from PySLSystemCalls import *

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
        self.mounted = is_server_mounted(self)

    @property
    def str_short(self):
        """ Return server info. Summary. """
        symbol = " [*]" if self.mounted is True else " [ ]"
        return "%s %s" % (symbol, self.name)

    @property
    def str_long(self):
        """ Return server info. Verbose. """
        return "%s --- %s@%s:%s on %s" % (self.str_short,
                                          self.details[USER],
                                          self.details[IP],
                                          self.details[PORT],
                                          self.details[LPATH])

    def mount( self ):
        """ Mount the server. """
        if not self.mounted:
            mdir = os.path.expanduser(self.details[LPATH])
            if os.path.isdir(mdir) is False:
                os.mkdir(mdir)

            self.mounted = sshfs(self.details[USER],
                                 self.details[IP],
                                 self.details[PORT],
                                 self.details[RPATH],
                                 mdir)

    def unmount( self ):
        """ Unmount the server. """
        if self.mounted:
            mdir = os.path.expanduser(self.details[LPATH])

            try:
                umount( mdir )
                self.mounted = False

                try:
                    os.rmdir(mdir)
                except OSError:
                    pass
            except PySLError as uex:
                print uex

    def ssh( self ):
        """ SSH into the server. """
        ssh(self.details[USER], self.details[IP], self.details[PORT] )
        return 1

def is_server_mounted(server):
    """ Checks if a server is mounted on the system. """
    return isMachineMounted(server.details[USER],
                            server.details[IP],
                            server.details[RPATH],
                            server.details[LPATH])

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

    def find_all_containing(self, name):
        """ Get the servers that have a name matching the provided term. """
        return [ s for s in self.servers if name in s.name ]

    def find(self, name):
        """ Get the first server that has a name matching the provided name. """
        return [ s for s in self.servers if name == s.name ][:1]
