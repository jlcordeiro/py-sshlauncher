""" Internal wrapper for mount options. """

import os
import errno
import subprocess
from subprocess import check_output
from subprocess import CalledProcessError

def ssh(suser, sip, sport):
    """ SSH into machine. """
    command = "ssh -p %d %s@%s" % (int(sport), suser, sip)
    os.system( command )

def sshfs(suser, sip, sport, spath, mountpoint):
    """ Mount machine using sshfs (os.system). """
    if os.path.isdir(mountpoint) == False:
        code = errno.ENOTDIR
        raise OSError(code, errno.errorcode[code])

    command = "sshfs -C -p %d %s@%s:%s %s" % (int(sport),
                                              suser,
                                              sip,
                                              spath,
                                              mountpoint)
    res = os.system( command )

    return (res == 0)

def is_machine_mounted(suser, sip, remotepath, localpath):
    """ Checks if a machine is mounted on the system already.
        Returns True if it is. False otherwise. """

    try:
        cmd_out = check_output("mount ", stderr=subprocess.STDOUT, shell=True)
    except CalledProcessError:
        code = errno.EREMOTEIO
        raise OSError(code, errno.errorcode[code])

    mount_list = cmd_out.decode("utf-8").split('\n')

    search_string = "%s@%s:%s on %s " % (suser,
                                         sip,
                                         remotepath,
                                         os.path.abspath(localpath))

    for item in mount_list:
        if item.find(search_string) is not -1:
            return True

    return False
