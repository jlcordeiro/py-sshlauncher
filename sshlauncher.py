#!/usr/bin/python

""" Quickly ssh/sftp/mount/unmount into another machine. """

import sys
import argparse
from sserver import valid_server
from sserver import SServerList


PARSER = argparse.ArgumentParser(description='Control ssh endpoints.')

PARSER.add_argument('--config-file',
                    dest='config_file', action='store',
                    nargs=1, metavar='CONFIG_FILE',
                    default='~/.remotes_config',
                    help='Configuration file to be user.')

# create the top-level parser
SUBPARSERS = PARSER.add_subparsers(help='sub-command help')

# list sub command

PARSER_LST = SUBPARSERS.add_parser('list', help='List servers.')

PARSER_LST.add_argument('list', nargs='?', metavar='FILTER',
                        help='List endpoints.')

PARSER_LST.add_argument('-v', '--verbose',
                        dest='verbose', action='store_true', default='false',
                        help='Verbose mode.')

PARSER_LST.add_argument('--state',
                        dest='filter_state', action='store',
                        metavar='STATE', default='any',
                        choices=['mounted','unmounted','any'],
                        help='Filter by state.')

# mount sub command

PARSER_MNT = SUBPARSERS.add_parser('mount', help='Mount servers.')

PARSER_MNT.add_argument('mount', nargs=1, metavar='ENDPOINT_NAME',
                        help='Mount the endpoint with the specified name.')

PARSER_MNT.add_argument('-a', '--all',
                        dest='all', action='store_true', default='false',
                        help='Mount endpoints matching the (optional) filter.')

# unmount sub command

PARSER_UMT = SUBPARSERS.add_parser('unmount', help='Unmount servers.')

PARSER_UMT.add_argument('unmount', nargs=1, metavar='ENDPOINT_NAME',
                        help='Unmount endpoints.')

PARSER_UMT.add_argument('-a', '--all',
                        dest='all', action='store_true', default='false',
                       help='Unmount endpoints matching the (optional) filter.')

# ssh sub command

PARSER_SSH = SUBPARSERS.add_parser('ssh', help='SSH into server.')

PARSER_SSH.add_argument('ssh', nargs=1, metavar='ENDPOINT_NAME',
                        help='SSH into endpoint.')

# sftp sub command

PARSER_SFTP = SUBPARSERS.add_parser('sftp', help='SFTP into server.')

PARSER_SFTP.add_argument('sftp', nargs=1, metavar='ENDOINT_NAME',
                        help='SFTP into endpoint.')

ARGS = PARSER.parse_args()

SERVERS = SServerList(ARGS.config_file)

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
            print server.str_short

    def __unmount_servers(self):
        """ Unmount all endpoints. """
        for server in self.endpoints:
            server.unmount()
            print server.str_short

    def __ssh(self):
        """ Connect into the first endpoint. """
        self.endpoints[0].ssh()

    def __sftp(self):
        """ SFTP into the first endpoint. """
        self.endpoints[0].sftp()

    def __list_servers(self):
        """ Prints all the endpoints.
            print mode - prints details if 'verbose',
            otherwise it just prints the server name """

        for server in self.endpoints:
            if self.name == "listv":
                print server.str_long
            else:
                print server.str_short

    def get_method(self):
        """Get the method to be run, from the action name."""

        return  {
                "list":         self.__list_servers,
                "listv":        self.__list_servers,
                "mount_all":    self.__mount_servers,
                "unmount_all":  self.__unmount_servers,
                "ssh":          self.__ssh,
                "sftp":         self.__sftp,
                "mount":        self.__mount_servers,
                "unmount":      self.__unmount_servers
                }[self.name]

    def run(self):
        """ Perform the action. """

        if self.endpoints is None or len(self.endpoints) < 1:
            return -1

        self.get_method()()
        return 0

def action_factory(args):
    """ Create an action based on the command arguments. """

    # Create the action
    action = None
    if "list" in args:
        a_filter = args.list if args.list else ""
        a_name = "listv" if args.verbose is True else "list"
        action = Action(a_name, a_filter)
    elif "ssh" in args:
        action = Action("ssh", args.ssh[0])
    elif "sftp" in args:
        action = Action("sftp", args.sftp[0])
    elif "mount" in args:
        a_name = "mount_all" if args.all is True else "mount"
        action = Action(a_name, args.mount[0])
    elif "unmount" in args:
        a_name = "unmount_all" if args.all is True else "unmount"
        action = Action(a_name, args.unmount[0])

    # Set the endpoints
    if action.name in ("mount_all", "unmount_all"):
        action.endpoints = SERVERS.find_all_containing(action.name_filter)
    elif action.name in ("ssh", "sftp", "mount", "unmount"):
        action.endpoints = SERVERS.find(action.name_filter)
    elif action.name in ("list", "listv"):
        endpoints_with_name = SERVERS.find_all_containing(action.name_filter)

        action.endpoints = [e for e in endpoints_with_name
                            if valid_server(e, ARGS.filter_state)]

    return action

if action_factory(ARGS).run() < 0:
    print "Server not found."
    sys.exit(1)

sys.exit(0)
