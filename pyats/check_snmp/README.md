# Overview

Validate SNMP settings

## Checks:
TODO
### Check for the following ntp servers in a 'show run':

```
snmp-server community XXXXXX RO
snmp-server host 172.22.192.56 XXXXX
```

# Running

```
pyats run job check_snmp_job.py --testbed-file ../testbed.yaml