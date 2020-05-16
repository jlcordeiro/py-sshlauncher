#!/usr/bin/python

""" Quickly ssh/sftp/mount/unmount into another machine. """

import os
import argparse
from sserver import SServer
from configobj import ConfigObj


# create the top-level parser
PARSER = argparse.ArgumentParser(description='Control ssh endpoints.')

PARSER.add_argument('--config-file',
                    dest='config_file', action='store',
                    nargs=1, metavar='CONFIG_FILE',
                    default='~/.remotes_config',
                    help='Configuration file to be user.')

SUBPARSERS = PARSER.add_subparsers(help='sub-command help')

# list sub command
PARSER_LST = SUBPARSERS.add_parser('list', help='List servers.')
PARSER_LST.add_argument('list', nargs='?', metavar='FILTER',
                        help='List endpoints.')

PARSER_MNT = SUBPARSERS.add_parser('mount', help='Mount servers.')
PARSER_MNT.add_argument('mount', nargs=1, metavar='ENDPOINT_NAME',
                        help='Mount the endpoint with the specified name.')

PARSER_UMT = SUBPARSERS.add_parser('unmount', help='Unmount servers.')
PARSER_UMT.add_argument('unmount', nargs=1, metavar='ENDPOINT_NAME',
                        help='Unmount endpoints.')

PARSER_SSH = SUBPARSERS.add_parser('ssh', help='SSH into server.')
PARSER_SSH.add_argument('ssh', nargs=1, metavar='ENDPOINT_NAME',
                        help='SSH into endpoint.')

PARSER_SFTP = SUBPARSERS.add_parser('sftp', help='SFTP into server.')
PARSER_SFTP.add_argument('sftp', nargs=1, metavar='ENDOINT_NAME',
                        help='SFTP into endpoint.')

ARGS = PARSER.parse_args()
CONFIG = ConfigObj(os.path.expanduser(ARGS.config_file))

class Action(object):
    """ Class representing a possible action. """

    def __init__(self, name, server_names):
        self.command_name = name

        self.servers = [SServer(cname, CONFIG[cname])
                         for cname in CONFIG
                         if cname in server_names or name == "list"]
        self.servers.sort(key=lambda s: s.name)


    def __mount_servers(self):
        """ Mount all endpoints. """
        for s in self.servers:
            s.mount()
            print(s.str_short)

    def __unmount_servers(self):
        """ Unmount all endpoints. """
        for s in self.servers:
            s.unmount()
            print(s.str_short)

    def __ssh(self):
        """ Connect into the first endpoint. """
        for s in self.servers:
            s.ssh()

    def __sftp(self):
        """ SFTP into the first endpoint. """
        for s in self.servers:
            s.sftp()

    def __list_servers(self):
        """ Prints all the endpoints. """
        for s in self.servers:
            print(s.str_long)

    def run(self):
        """ Perform the action. """

        if self.servers is None or len(self.servers) < 1:
            print("Server not found.")
            return -1

        {
            "list":         self.__list_servers,
            "ssh":          self.__ssh,
            "sftp":         self.__sftp,
            "mount":        self.__mount_servers,
            "unmount":      self.__unmount_servers
        }[self.command_name]()

def action_factory(args):
    """ Create an action based on the command arguments. """
    # Create the action
    if "list" in args:
        action = Action("list", "")
    elif "ssh" in args:
        action = Action("ssh", args.ssh)
    elif "sftp" in args:
        action = Action("sftp", args.sftp)
    elif "mount" in args:
        action = Action("mount", args.mount)
    elif "unmount" in args:
        action = Action("unmount", args.unmount)

    return action

if __name__ == "__main__":
    action_factory(ARGS).run()
