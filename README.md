py-sshlauncher
==============

Quickly ssh/mount/unmount into another machine (by name from a list of known machines)

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
  -s ENDPOINT_NAME, --ssh ENDPOINTNAME
                        SSH into endpoint.
  -m ENDPOINT_NAME, --mount ENDPOINTNAME
                        Mount endpoints.
  -u ENDPOINT_NAME, --unmount ENDPOINTNAME
                        Unmount endpoints.
  --config-file CONFIG_FILE
                        Configuration file to be user.
