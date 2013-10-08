#!/usr/bin/python

import sys
import argparse
from sserver import SServerList

parser = argparse.ArgumentParser(description='Control ssh endpoints.')
parser.add_argument('-a', '--all', dest='mount_all', action='store', nargs='?', const='', metavar='FILTER',
                   help='Mount all endpoints matching the (optional) filter.')
parser.add_argument('-n', '--none', dest='unmount_all', action='store', nargs='?', const='', metavar='FILTER',
                   help='Unmount all endpoints matching the (optional) filter.')
parser.add_argument('-l', '--list', dest='list', action='store', nargs='?', const='', metavar='FILTER',
                   help='List endpoints.')
parser.add_argument('--format', dest='list_format', action='store', metavar='FORMAT',
                   choices=['normal','verbose'], default='normal',
                   help='Format used to print endpoints.')
parser.add_argument('--state', dest='filter_state', action='store', metavar='STATE',
                   choices=['mounted','unmounted','any'], default='any',
                   help='Filter printed endpoints by state.')
parser.add_argument('-s', '--ssh', dest='ssh', action='store', nargs=1, metavar='ENDPOINT_NAME',
                   help='SSH into endpoint.')
parser.add_argument('-m', '--mount', dest='mount', action='store', nargs=1, metavar='ENDPOINT_NAME',
                   help='Mount endpoints.')
parser.add_argument('-u', '--unmount', dest='unmount', action='store', nargs=1, metavar='ENDPOINT_NAME',
                   help='Unmount endpoints.')
parser.add_argument('--config-file', dest='config_file', action='store', nargs=1, metavar='CONFIG_FILE', default='~/.remotes_config',
                   help='Configuration file to be user.')

args = parser.parse_args()

servers = SServerList()
servers.add_from_config( args.config_file )

if args.list is not None:
   servers.print_list( args.list, args.filter_state, args.list_format )
elif args.mount_all is not None:
   for server in servers.find_all(partial_match=args.mount_all):
      server.mount()
      server.Print()
elif args.unmount_all is not None:
   for server in servers.find_all(partial_match=args.unmount_all):
      server.unmount()
      server.Print()
elif args.ssh:
   server = servers.find_all(exact_match=args.ssh[0])[0]
   if server is not None:
      server.ssh()
elif args.mount:
   server = servers.find_all(exact_match=args.mount[0])[0]
   if server is not None:
      server.mount()
elif args.unmount:
   server = servers.find_all(exact_match=args.unmount[0])[0]
   if server is not None:
      server.unmount()
else:
   sys.exit(1)

sys.exit(0)
