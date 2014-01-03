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

ARGS = parser.parse_args()

SERVERS = SServerList()
SERVERS.add_from_config( ARGS.config_file )

class Action:
    def __init__(self, name, name_filter):
        self.name = name
        self.name_filter = name_filter
        self.endpoints = []


    def __mount_servers(self):
        """ Mount all servers in a list. """
        for server in self.endpoints:
            server.mount()
            server.Print()

    def __unmount_servers(self):
        """ Unmount all servers in a list. """
        for server in self.endpoints:
            server.unmount()
            server.Print()

    def __ssh(self):
        self.endpoints[0].ssh()

    def __list_servers(self):
        SERVERS.print_list(self.name_filter, ARGS.filter_state, ARGS.list_format)

    def run(self):
        if self.endpoints is None:
            return -1

        {
            "list":         self.__list_servers,
            "mount_all":    self.__mount_servers,
            "unmount_all":  self.__unmount_servers,
            "ssh":          self.__ssh,
            "mount":        self.__mount_servers,
            "unmount":      self.__unmount_servers
        }[self.name]()

        return 0

def action_factory(args):
    """ Create an action based on the command arguments. """

    # Create the action
    action = None
    if args.list is not None:
        action = Action("list", args.list)
    elif args.mount_all is not None:
        action = Action("mount_all", args.mount_all)
    elif args.unmount_all is not None:
        action = Action("unmount_all", args.unmount_all)
    elif args.ssh:
        action = Action("ssh", args.ssh[0])
    elif args.mount:
        action = Action("mount", args.mount[0])
    elif args.unmount:
        action = Action("unmount", args.unmount[0])

    # Set the endpoints
    if action.name in ("mount_all", "unmount_all"):
        action.endpoints = SERVERS.find_all(partial_match=action.name_filter)
    elif action.name in ("ssh", "mount", "unmount"):
        action.endpoints = [SERVERS.find_one(exact_match=action.name_filter)]

    return action


if action_factory(ARGS).run() < 0:
    print "Server not found."
    sys.exit(1)

sys.exit(0)
