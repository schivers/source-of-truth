# WORK IN PROGRESS 

# Overview

This test job attempts to verify the following:

- Hostname
- Configured credentials
- Domain Name Configuration
- Crypto Key Existence 
- SSH Version
- 'transport input ssh' under line vty 0
- AAA settings
- Enable Secret

# Running

```
pyats run job remote_manage_job.py --testbed-file ../testbed.yaml