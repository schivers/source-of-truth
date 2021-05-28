# Overview

Validate the Core router's downlink connection torwards the Core switches

## Checks:
1) Checks global eigrp neighbours table
2) Checks each VRF eighrp neighbours table 

Both checks must have exactly 3 EIGRP neighbours.


# Running

```
pyats run job eigrp_test_job.py --testbed-file ../testbed.yaml