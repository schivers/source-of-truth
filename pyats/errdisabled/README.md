# Overview

This test job attempts to validate the errdisabled recovery feature configuration.

## Command

`show run | include ^errdisable`

## Check

Configuration must have the following:

```
"errdisable recovery cause udld",
"errdisable recovery cause bpduguard",
"errdisable recovery cause mac-limit",
"errdisable recovery cause storm-control",
"errdisable recovery interval 900"
```

## Running

```
pyats run job errdisabled_test_job.py --testbed-file ../testbed.yaml