""" Internal wrapper for mount options. """

import os
import errno
from subprocess import check_call, CalledProcessError


def ssh(suser, sip, sport):
    """ SSH into machine. """
    command = "ssh -p %d %s@%s" % (int(sport), suser, sip)
    os.system(command)

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
    return os.system(command) == 0


def sftp(suser, sip, sport, spath):
    """ SFTP into machine. """
    command = "sftp -P%d %s@%s:%s" % (int(sport), suser, sip, spath)
    os.system(command)


def unmount(mountpoint):
    """ Unmount point without root permissions. """
    try:
        check_call(['fusermount', '-u', mountpoint])
    except CalledProcessError, cpe:
        raise OSError(cpe.returncode, "fusermount failed. " + str(cpe.output))
