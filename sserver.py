import os

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

      result = sshfs( self.username, self.ip, self.port, self.remotepath, self.mountpoint )
      if result == True:
         self.mounted = True
         return 1

      return 0

   def unmount( self ):
      if self.mounted is False:
         return 0

      result = umount( self.mountpoint )
      if result == True:
         self.mounted = False
         return 1

      return 0

   def ssh( self ):
      ssh( self.username, self.ip, self.port )
      return 1

