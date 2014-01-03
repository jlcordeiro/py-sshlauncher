import os
from configobj import ConfigObj
from PySLSystemCalls import *

class SServer():
   def __init__(self, name, mountpoint, username, ip, remotepath, port):
        self.name = name
        self.mountpoint = mountpoint
        self.username = username
        self.ip = ip
        self.remotepath = remotepath
        self.port = port
        self.mounted = False
  
   def mountString( self ):
      return " [*] " if self.mounted is True else " [ ] "

   def Print( self ):
      print self.mountString() + self.name

   def PrintDetails( self ):
      print self.mountString() + self.name + " --- " + self.username + "@" + self.ip + ":" + self.port + " on " + self.mountpoint

   def mount( self ):
      if self.mounted is True:
         return 0

      mdir = os.path.expanduser(self.mountpoint)

      if os.path.isdir(mdir) is False:
         os.mkdir(mdir)

      result = sshfs( self.username, self.ip, self.port, self.remotepath, mdir )
      if result == True:
         self.mounted = True
         return 1

      return 0

   def unmount( self ):
      if self.mounted is False:
         return 0

      mdir = os.path.expanduser(self.mountpoint)

      try:
         umount( mdir )

         self.mounted = False

         try:
             os.rmdir(mdir)
         except OSError as rex:
            pass

         return 1
      except PySLError as uex:
         print uex

      return 0

   def ssh( self ):
      ssh( self.username, self.ip, self.port )
      return 1

def isServerMounted( server ):
   """ Checks if a server is mounted on the system. """
   return isMachineMounted( server.username, server.ip, server.remotepath, server.mountpoint )

class SServerList():
   def __init__( self ):
      self.servers = []

   def add_from_config( self, filename ):
      """ Append all servers found on the configuration file to the local list of servers. """
         
      final_path = os.path.expanduser(filename)
      config = ConfigObj( final_path )

      for c in config:
         ip = config[c]["ip"]
         port = config[c]["port"]
         user = config[c]["user"]
         remotepath = config[c]["remotepath"]
         mountpoint = config[c]["mountpoint"]

         new_server = SServer( c, mountpoint, user, ip, remotepath, port )
         new_server.mounted = isServerMounted( new_server )

         self.servers.append( new_server )

   def find_all( self, exact_match=None, partial_match=None ):
      """ Get the servers that have a name matching the parameters.
         If exact_match is provided, returns the ones that match that exact string.
         Otherwise, returns the servers that have a name including that string. """
      if exact_match is not None:
         return [ s for s in self.servers if exact_match == s.name ]

      if partial_match is not None:
         return [ s for s in self.servers if partial_match in s.name ]

      return []

   def find_one( self, exact_match=None, partial_match=None ):
      """ Get the first server that has a name matching the parameters.
         If exact_match is provided, returns one that match that exact string.
         Otherwise, returns one that has a name including that string. """

      matches = self.find_all(exact_match,partial_match)

      if len(matches) < 1:
         return None

      return matches[0]

def valid_server(server, wanted_state):
    """ Tells whether or not a server is in the wanted state.
        The possible values for wanted_state are
        ('any', 'mounted', 'unmounted') """

    if wanted_state == 'any':
        return True

    if wanted_state == 'mounted' and server.mounted is True:
        return True

    if wanted_state == 'unmounted' and server.mounted is False:
        return True

    return False

