# Overview

This test job attempts Verify VTP settings (VTP mode and domain)

## Checks:
1) VTP Domain Name = Device Hostname
2) VTP Operating Mode = Transparent


# Running

```
pyats run job check_syslog_job.py --testbed-file ../testbed.yaml