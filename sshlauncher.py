#!/usr/bin/python

""" Quickly ssh/sftp/mount/unmount into another machine. """

import os
import sys
import json

COMMANDS = {"list":     ("echo \"{_name} {_user}@{_ip}:{_port} on {_mountpoint}\"", "opt:apply_to_all"),
            "mount":    ("mkdir -p {_mountpoint} && sshfs -C -p {_port} {_user}@{_ip}:{_remotepath} {_mountpoint}",),
            "unmount":  ("fusermount -u {_mountpoint}; rmdir {_mountpoint}",),
            "sftp":     ("sftp -P{_port} {_user}@{_ip}:{_remotepath}",),
            "yafc":     ("yafc sftp://{_user}@{_ip}:{_port}/{_remotepath}",),
            "ssh":      ("ssh -p {_port} {_user}@{_ip}",),
            "mysql":    ("mysql -h{_ip} -u{_user} -P{_port} -p {_database}",)
           }

def run_command(config, command_name, endpoint_name):
    """ Run a command on the specified endpoint. """

    ep_details = config[endpoint_name]

    cmd = COMMANDS[command_name][0]
    for placeholder in ("{_port}", "{_user}", "{_ip}", "{_remotepath}", "{_database}", "{_name}", "{_mountpoint}"):
        value = ep_details[placeholder[1:-1]] if placeholder[1:-1] in ep_details else ""
        cmd = cmd.replace(placeholder, value)

    os.system(cmd)


def command_applies_to_all(command_name):
    """
    Returns whether or not the command with the given name should
    be ran for all the endpoints in the configuration file (True)
    or only for the endpoints provided as parameter (False)
    """
    return "opt:apply_to_all" in COMMANDS[command_name]



if __name__ == "__main__":
    available_commands = COMMANDS.keys()
    if len(sys.argv) < 2 or sys.argv[1] not in available_commands:
        print("usage: {} {{{}}} (ep1, ep2, ...)".format(sys.argv[0],
                                                ",".join(available_commands)))
        sys.exit(1)

    (command_name, endpoints) = (sys.argv[1], sys.argv[2:])
    with open(os.path.expanduser('~/.remotes_config.json')) as json_file:
        config = json.load(json_file)

    for ep in config:
        if ep in endpoints or command_applies_to_all(command_name):
            run_command(config, command_name, ep)
