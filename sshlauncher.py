#!/usr/bin/python

""" Quickly ssh/sftp/mount/unmount into another machine. """

import os
import sys
from sserver import SServer
from configobj import ConfigObj


CONFIG = ConfigObj(os.path.expanduser('~/.remotes_config'))

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

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("usage: {} {list,mount,unmount,ssh,sftp} [ep1, ep2, ...]", sys.argv[0])
        sys.exit(1)

    (command, endpoints) = (sys.argv[1], sys.argv[2:])
    action = Action(command, endpoints)
    action.run()
