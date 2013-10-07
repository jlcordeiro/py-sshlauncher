import os
from configobj import ConfigObj

def ssh( user, ip, port ):
   os.system( "ssh -p " + port + " " + user + "@" + ip )

def sshfs( user, ip, port, path, mountpoint ):
   res = os.system( "sshfs -C -p " + port + " " + user + "@" + ip + ":" + path + " " + mountpoint )

   if res == 0:
      return True

   return False

def umount( mountpoint ):
   res = os.system( "umount " + mountpoint )

   if res == 0:
      return True
   
   return False

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

      result = umount( mdir )
      if result == True:
         self.mounted = False

         try:
             os.rmdir(mdir)
         except OSError as ex:
            pass

         return 1

      return 0

   def ssh( self ):
      ssh( self.username, self.ip, self.port )
      return 1

class SServerList():
   def __init__( self ):
      self.servers = []

   def mark_mounted( self ):
      """ Run trought the servers and mark as mounted those that are found in /etc/mtab. """
      # read mtab into memory
      mtab = open( "/etc/mtab", "r" )
      mtabText = mtab.read()
      mtab.close()

      # check which servers are in there
      for s in self.servers:
         s.mounted = mtabText.find( s.username + "@" + s.ip + ":" + s.remotepath) is not -1

   def add_from_config( self, filename ):
         
      final_path = os.path.expanduser(filename)
      config = ConfigObj( final_path )

      for c in config:
         ip = config[c]["ip"]
         port = config[c]["port"]
         user = config[c]["user"]
         remotepath = config[c]["remotepath"]
         mountpoint = config[c]["mountpoint"]

         self.servers.append( SServer( c, mountpoint, user, ip, remotepath, port ) )

      self.mark_mounted()

   def print_list( self, namefilter='', state='any', printmode='' ):
      """ prints the list of servers.
         namefilter - used to filter the servers by name. Only those that have the filter string on
         on their name are printed
         state- used to filter the servers by their state.
            * any - all servers are printed
            * mounted - only mounted servers are printed
            * unmounted - only unmounted servers are printed
         print mode - prints details if 'verbose', otherwise it just prints the server name """

      for s in self.servers:
         if namefilter in s.name:

            if state=='mounted' and s.mounted is False:
               continue

            if state=='unmounted' and s.mounted is True:
               continue

            if printmode == "verbose":
               s.PrintDetails()
            else:
               s.Print()

   def find_all( self, exact_match=None, partial_match=None ):
      """ Get the servers that have a name matching the parameters.
         If exact_match is provided, returns the ones that match that exact string.
         Otherwise, returns the servers that have a name including that string. """
      if exact_match is not None:
         return [ s for s in self.servers if exact_match == s.name ]

      if partial_match is not None:
         return [ s for s in self.servers if partial_match in s.name ]

      return []
