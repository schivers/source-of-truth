# Overview

This check connects to all devices defined in the testbed, and parses locally configured
usernames against a list provided at runtime, the test passes if all usernames (an no additional)
users are configured on the device.


17/06/2021 - Created V2 of this script to test by default (no arguments) for the following users: 

netbox admin solarwinds 

The script logic has changed as well- It now makes sure the supplied list is in found in the configuration but will not fail if other users are found. (Original did this)



## Running
```
pyats run job local_user_check_job.py  --mail-to shaun.chivers@global.ntt --mail-html --submitter shaunchivers --testbed-file ../testbed.yaml --html_logs --webex-token OTBlNDk4NTctMWMwZC00MzE1LWEwOWItYmJkNWU5MjAzZWNiODMzNDE1OTAtOGEz_PF84_0198f08a-3880-4871-b55e-4863ccf723d5 --webex-space Y2lzY29zcGFyazovL3VzL1JPT00vNTIxOWRiYTAtYWNiMC0xMWViLTgzYjctOTVlMTRhZTBhYTE3 --local_users admin netbox murad rustam elmar allazov shaun
```