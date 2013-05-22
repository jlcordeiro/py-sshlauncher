import sserver
from configobj import ConfigObj

def ReadConfigIntoList( filename ):
   config = ConfigObj( filename )

   serverList = []

   for c in config:
      name = c
      ip = config[c]["ip"]
      port = config[c]["port"]
      user = config[c]["user"]
      remotepath = config[c]["remotepath"]
      mountpoint = config[c]["mountpoint"]

      serverList.append( sserver.SServer( name, mountpoint, user, ip, remotepath, port ) )

   return serverList

