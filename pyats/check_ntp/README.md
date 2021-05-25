# Overview

Check NTP settings and association

## Checks:
TODO
### Check for the following ntp servers in a 'show run':

```
BAKTVC1SWD01#sho run | in ntp
ntp server 172.22.192.56
ntp server 10.224.0.100 prefer
```

### Check for 'synchronised' in the output of a 'show ntp status'

```
BAKMTR1SWC01#sho ntp status 
Clock is unsynchronized, stratum 16, no reference clock
nominal freq is 250.0000 Hz, actual freq is 250.0000 Hz, precision is 2**10
ntp uptime is 114780700 (1/100 of seconds), resolution is 4000
reference time is 00000000.00000000 (01:00:00.000 EURO Mon Jan 1 1900)
clock offset is 0.0000 msec, root delay is 0.00 msec
root dispersion is 17216.75 msec, peer dispersion is 0.00 msec
loopfilter state is 'FSET' (Drift set from file), drift is 0.000000000 s/s
system poll interval is 8, never updated.
```

# Running

```
pyats run job check_ntp_job.py --testbed-file ../testbed.yaml