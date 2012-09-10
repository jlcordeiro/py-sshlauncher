import os
from PySLErrors import *


def ssh( user, ip, port ):
   command = "ssh -p %d %s@%s" % ( int(port), user, ip )
   os.system( command )

def sshfs( user, ip, port, path, mountpoint ):
   if os.path.isdir(mountpoint) == False:
	   raise PySLDirNotFoundError

   command = "sshfs -C -p %d %s@%s:%s %s" % ( int(port), user, ip, path, mountpoint )
   os.system( command )

def umount( mountpoint ):
   os.system( "umount " + mountpoint )

def serverIsMounted( user, ip, remotepath, localpath):

   searchString = "%s@%s:%s %s " % ( user, ip, remotepath, localpath )

   mtab = open( "/etc/mtab", "r" )
   exists = mtab.read().find( searchString ) is not -1
   mtab.close()

   return exists
