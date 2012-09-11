import os
import sys
import subprocess
from subprocess import *
from PySLErrors import *

def createMountPoint( localpath ):
   """ Function that creates the mountpoint for a machine. If the folder already exists nothing is done. """
   if os.path.isdir( localpath ) == True:
      return

   os.makedirs( localpath )

def ssh( user, ip, port ):
   command = "ssh -p %d %s@%s" % ( int(port), user, ip )
   os.system( command )

def sshfs( user, ip, port, path, mountpoint ):
   if os.path.isdir(mountpoint) == False:
	   raise PySLDirNotFoundError

   command = "sshfs -C -p %d %s@%s:%s %s" % ( int(port), user, ip, path, mountpoint )
   os.system( command )

def umount( mountpoint ):
   """ Unmounts a directory. If the operation is not successfull it will raise an exception.
         Raises PySLDirNotMountedError is the directory is found but is not a mountpoint,
         PySLNoPermissionsError if the user does not have enough permissions to unmount,
         PySLDirNotFoundError if the directory is not found
         or a general PySLError for any other issue."""
   fullpath = os.path.abspath(mountpoint)
   try:
      res = check_output( "umount " + fullpath, stderr=subprocess.STDOUT, shell=True )
   except CalledProcessError as e:
      notMountedString1    = "umount: %s is not mounted (according to mtab)" % fullpath
      notMountedString2    = "umount: %s: not mounted" % fullpath
      notFoundString       = "umount: %s: not found" % fullpath
      noPermissionString   = "umount: %s is not in the fstab (and you are not root)" % fullpath

      if notMountedString1 in str(e.output) or notMountedString2 in str(e.output):
         raise PySLDirNotMountedError

      if noPermissionString in str(e.output):
         raise PySLNoPermissionsError

      if notFoundString in str(e.output):
         raise PySLDirNotFoundError

      raise PySLError(0,str(e.output))

def serverIsMounted( user, ip, remotepath, localpath):

   searchString = "%s@%s:%s %s " % ( user, ip, remotepath, os.path.abspath(localpath) )

   mtab = open( "/etc/mtab", "r" )
   exists = mtab.read().find( searchString ) is not -1
   mtab.close()

   return exists


#### unit testing

if __name__ == "__main__":
   
   ## local machine details
 
   ip = "10.1.10.150"
   port = 22
   user = "joao"
   remotepath = "."
   localpath = "./mnt"


   ## prepare system

   # unmount server
   try:
      umount(localpath)
   except PySLNoPermissionsError as e:
      print("You don't have permissions to run these tests.")
      sys.exit(1)
   except PySLError as e:
      pass

   #delete mount points
   try:
      os.removedirs( localpath )
   except:
      pass


   ## test

   # check server is not mounted
   assert serverIsMounted( user, ip, remotepath, localpath ) == False

   # mount server. should fail because folder has not been mounted
   try:
      sshfs( user, ip, port, remotepath, localpath )
      raise AssertionError
   except PySLDirNotFoundError:
      pass

   # check server is still not mounted
   assert serverIsMounted( user, ip, remotepath, localpath ) == False

   # create folder
   createMountPoint( localpath )
   createMountPoint( localpath ) # create folder again, to make sure it is checking that the folder already exists

   # try to mount again
   sshfs( user, ip, port, remotepath, localpath )

   # server should now be mounted
   assert serverIsMounted( user, ip, remotepath, localpath ) == True
   
   # unmount server
   try:
      umount(localpath)
   except PySLNoPermissionsError as e:
      print("You don't have permissions to run these tests.")
      sys.exit(1)

   # check server is still not mounted
   assert serverIsMounted( user, ip, remotepath, localpath ) == False

   # unmount server -- error casess
   # already unmounted
   try:
      umount(localpath)
      raise AssertionError
   except PySLNoPermissionsError as e:
      print("You don't have permissions to run these tests.")
      sys.exit(1)
   except PySLDirNotMountedError:
      pass

   # deleted
   os.removedirs( localpath )
   try:
      umount(localpath)
      raise AssertionError
   except PySLNoPermissionsError as e:
      print("You don't have permissions to run these tests.")
      sys.exit(1)
   except PySLDirNotFoundError:
      pass

   print("[PySLSystemCalls] System calls testing complete.")
