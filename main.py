#!/usr/bin/python

import sys
from sys import argv

import config

configfile = "/home/joao/.remotes_config"

EXIT_SUCCESS = 0
EXIT_FAILURE = 1

def markMountedServers( sl ):
   # read mtab into memory
   mtab = open( "/etc/mtab", "r" )
   mtabText = mtab.read()
   mtab.close()

   # check which servers are in there
   for s in sl:
      s.mounted = mtabText.find( s.username + "@" + s.ip + ":" + s.remotepath) is not -1

def printlist( namefilter='', mounted='any', printmode='' ):
   """ prints the list of servers.
      namefilter - used to filter the servers by name. Only those that have the filter string on
      on their name are printed
      mounted - used to filter the servers by their state.
         * any - all servers are printed
         * yes - only mounted servers are printed
         * no - only unmounted servers are printed
      print mode - prints details if 'verbose', otherwise it just prints the server name """

   for s in serverList:
      if namefilter in s.name:

         if mounted=='yes' and s.mounted is False:
            continue

         if mounted=='no' and s.mounted is True:
            continue

         if printmode == "verbose":
            s.PrintDetails()
         else:
            s.Print()

def printOptions():
   print "USAGE: " + sys.argv[0] + " <command> <rremote>"
   print
   print "Commands:"
   print "    list [filter]         - List all remotes, indicating which are mounted and filtering by filter"
   print "    listm [filter]        - List all mounted remotes and filtering by filter"
   print "    listu [filter]        - List all unmounted remotes and filtering by filter"
   print "    listdetails [filter]  - List all remotes, indicating which are mounted. With full details."
   print "    ssh                   - SSH into the specified remote"
   print "    mount                 - Mount the specified remote (if not already mounted)"
   print "    unmount                - Unmount the specified remote (if mounted)"
   print "    all                   - Mount all unmounted remotes"
   print "    none                  - Unmount all mounted remotes"  

minarguments = { "list"         : 2,
               "listm"        : 2,
               "listu"        : 2,
               "listdetails"  : 2,
               "none"         : 2,
               "all"          : 2,
               "mount"        : 3,
               "unmount"      : 3,
               "ssh"          : 3
             }

if len(argv) is 1 or sys.argv[1] == "help":
   printOptions()
   sys.exit(EXIT_SUCCESS)

serverList = config.ReadConfigIntoList( configfile )
markMountedServers(serverList)


###
### check argument validity
###

option = sys.argv[1]

try:
   if minarguments[option] > len(argv):
      printOptions()
except KeyError:
   printOptions()

###
### global options 
###

if "list" in option:

   namefilter = '' if len(argv)==2 else argv[2]
   printmode = 'verbose' if option == "listdetails" else ''
   mounted = 'yes' if option == "listm" else ( 'no' if option == "listu" else 'any' )

   printlist( namefilter, mounted, printmode )
   sys.exit(EXIT_SUCCESS)

if "none" in option:
   namefilter = '' if len(argv)==2 else argv[2]
   
   for s in serverList:
      if namefilter in s.name:
         s.unmount()
         s.Print()

   sys.exit(EXIT_SUCCESS)

if "all" in option:
   namefilter = '' if len(argv)==2 else argv[2]
   
   for s in serverList:
      if namefilter in s.name:
         s.mount()
         s.Print()

   sys.exit(EXIT_SUCCESS)

###
### server options 
###

if len(argv) == 3 :

   serverFound = False

   servername = sys.argv[2]
   for s in serverList:
      if s.name != servername:
         continue

      serverFound = True

      if option == "unmount":
            s.unmount()

      if option == "mount":
            s.mount()

      if option == "ssh":
            s.ssh()

   if serverFound is not True:
      print "Server not found."
