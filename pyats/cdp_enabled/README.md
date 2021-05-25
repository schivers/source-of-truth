# Overview

Verify that CDP is enabled globally

## Command:
  
`Show cdp neighbors` - note: The test uses the Pyats API `verify_cdp_in_state` which supports (IOS,XE,XR,NXOS)

## Checks:
The API call returns a boolean(true/false) to verify if CDP is enabled.


# Running

```
pyats run job cdp_enabled.py --testbed-file ../testbed.yaml