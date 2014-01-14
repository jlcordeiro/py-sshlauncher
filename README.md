py-sshlauncher
==============

Quickly ssh/mount/unmount into another machine (by name from a list of known machines)

Dependencies
============

libpymount
sshfs

Installing
==========

python setup.py install

Getting help
============

sshlauncher.py -h

```
usage: sshlauncher.py [-h] [--config-file CONFIG_FILE]
                      {list,mount,unmount,ssh} ...

Control ssh endpoints.

positional arguments:
  {list,mount,unmount,ssh}
                        sub-command help
    list                List servers.
    mount               Mount servers.
    unmount             Unmount servers.
    ssh                 SSH into server.

optional arguments:
  -h, --help            show this help message and exit
  --config-file CONFIG_FILE
                        Configuration file to be user.
```

List
----

Existing endpoints can be listed in as summary or in verbose mode. In both cases, it is possible to filter them by name or by state (mounted or unmounted).

```
usage: sshlauncher.py list [-h] [-v] [--state STATE] [FILTER]

positional arguments:
  FILTER         List endpoints.

optional arguments:
  -h, --help     show this help message and exit
  -v, --verbose  Verbose mode.
  --state STATE  Filter by state.
```

SSH
---

You can ssh into one of the servers, using its name.

```
usage: sshlauncher.py ssh [-h] ENDPOINT_NAME

positional arguments:
  ENDPOINT_NAME  SSH into endpoint.

optional arguments:
  -h, --help     show this help message and exit

```

Mount
-----

You can mount one of the servers (if using its name) or multiple servers (by using the --all flag and a term to filter the server names by).

```
usage: sshlauncher.py mount [-h] [-a] ENDPOINT_NAME

positional arguments:
  ENDPOINT_NAME  Mount the endpoint with the specified name.

optional arguments:
  -h, --help     show this help message and exit
  -a, --all      Mount endpoints matching the (optional) filter.
```

Unmount
-------

You can unmount one of the servers (if using its name) or multiple servers (by using the --all flag and a term to filter the server names by).

```
usage: sshlauncher.py unmount [-h] [-a] ENDPOINT_NAME

positional arguments:
  ENDPOINT_NAME  Unmount endpoints.

optional arguments:
  -h, --help     show this help message and exit
  -a, --all      Unmount endpoints matching the (optional) filter.
```
