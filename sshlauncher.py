#!/usr/bin/python

""" Quickly ssh/mount/unmount into another machine. """

import sys
import argparse
from sserver import valid_server
from sserver import SServerList

PARSER = argparse.ArgumentParser(description='Control ssh endpoints.')

PARSER.add_argument('-a', '--all',
                    dest='mount_all', action='store',
                    nargs='?', const='', metavar='FILTER',
                    help='Mount endpoints matching the (optional) filter.')

PARSER.add_argument('-n', '--none',
                    dest='unmount_all', action='store',
                    nargs='?', const='', metavar='FILTER',
                    help='Unmount endpoints matching the (optional) filter.')

PARSER.add_argument('-l', '--list',
                    dest='list', action='store',
                    nargs='?', const='', metavar='FILTER',
                    help='List endpoints.')

PARSER.add_argument('--format',
                    dest='list_format', action='store',
                    metavar='FORMAT', default='normal',
                    choices=['normal','verbose'],
                    help='Format used to print endpoints.')

PARSER.add_argument('--state',
                    dest='filter_state', action='store',
                    metavar='STATE', default='any',
                    choices=['mounted','unmounted','any'],
                    help='Filter printed endpoints by state.')

PARSER.add_argument('-s', '--ssh',
                    dest='ssh', action='store',
                    nargs=1, metavar='ENDPOINT_NAME',
                    help='SSH into endpoint.')

PARSER.add_argument('-m', '--mount',
                    dest='mount', action='store',
                    nargs=1, metavar='ENDPOINT_NAME',
                    help='Mount endpoints.')

PARSER.add_argument('-u', '--unmount',
                    dest='unmount', action='store',
                    nargs=1, metavar='ENDPOINT_NAME',
                    help='Unmount endpoints.')

PARSER.add_argument('--config-file',
                    dest='config_file', action='store',
                    nargs=1, metavar='CONFIG_FILE',
                    default='~/.remotes_config',
                    help='Configuration file to be user.')

ARGS = PARSER.parse_args()

SERVERS = SServerList()
SERVERS.add_from_config( ARGS.config_file )

class Action(object):
    """ Class representing a possible action. """

    def __init__(self, name, name_filter):
        self.name = name
        self.name_filter = name_filter
        self.endpoints = []

    def __mount_servers(self):
        """ Mount all endpoints. """
        for server in self.endpoints:
            server.mount()
            server.print_short()

    def __unmount_servers(self):
        """ Unmount all endpoints. """
        for server in self.endpoints:
            server.unmount()
            server.print_short()

    def __ssh(self):
        """ Connect into the first endpoint. """
        self.endpoints[0].ssh()

    def __list_servers(self):
        """ Prints all the endpoints.
            print mode - prints details if 'verbose',
            otherwise it just prints the server name """

        for server in self.endpoints:
            if ARGS.list_format == "verbose":
                server.print_details()
            else:
                server.print_short()

    def get_method(self):
        """Get the method to be run, from the action name."""

        return  {
                "list":         self.__list_servers,
                "mount_all":    self.__mount_servers,
                "unmount_all":  self.__unmount_servers,
                "ssh":          self.__ssh,
                "mount":        self.__mount_servers,
                "unmount":      self.__unmount_servers
                }[self.name]

    def run(self):
        """ Perform the action. """

        if self.endpoints is None:
            return -1

        self.get_method()()
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
    elif action.name == "list":
        endpoints_with_name = SERVERS.find_all(partial_match=action.name_filter)

        action.endpoints = [e for e in endpoints_with_name
                            if valid_server(e, ARGS.filter_state)]

    return action

if action_factory(ARGS).run() < 0:
    print "Server not found."
    sys.exit(1)

sys.exit(0)
