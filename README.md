py-sshlauncher
==============

Quickly ssh/mount/unmount into another machine (by name from a list of known machines)

Installing
==========

python setup.py install

Getting help
============

sshlauncher.py -h

```
usage: sshlauncher.py [-h] [-a [FILTER]] [-n [FILTER]] [-l [FILTER]]
                      [--format FORMAT] [--state STATE] [-s ENDPOINT_NAME]
                      [-m ENDPOINT_NAME] [-u ENDPOINT_NAME]
                      [--config-file CONFIG_FILE]

Control ssh endpoints.

optional arguments:
  -h, --help            show this help message and exit
  -a [FILTER], --all [FILTER]
                        Mount all endpoints matching the (optional) filter.
  -n [FILTER], --none [FILTER]
                        Unmount all endpoints matching the (optional) filter.
  -l [FILTER], --list [FILTER]
                        List endpoints.
  --format FORMAT       Format used to print endpoints.
  --state STATE         Filter printed endpoints by state.
  -s ENDPOINT_NAME, --ssh ENDPOINT_NAME
                        SSH into endpoint.
  -m ENDPOINT_NAME, --mount ENDPOINT_NAME
                        Mount endpoints.
  -u ENDPOINT_NAME, --unmount ENDPOINT_NAME
                        Unmount endpoints.
  --config-file CONFIG_FILE
                        Configuration file to be user.
```
