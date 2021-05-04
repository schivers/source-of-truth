## Webex Teams Bot
PyATS can notify job completion into Webex Teams

Create a Bot account from within your Webex account and grab the token and roomId.

Note: 
The Token is provided when you set up the Bot.
Use https://developer.webex.com/docs/api/v1/rooms/list-rooms to get the roomId.

Reference - https://developer.cisco.com/codeexchange/github/repo/hpreston/nxos-netbox-sync

Then run PyATS with the --webex-token and --webex-space keys

```
pyats run job Baku_test_job.py --mail-to shaun.chivers@global.ntt --mail-html --submitter shaunchivers --archive-dir /home/ntt/ftp/PyATS_Reports/ -t testbed.yaml --webex-token OTBlNDk4NTctMWMwZC00MzE1LWEwOWItYmJkNWU5MjAzZWNiODMzNDE1OTAtOGEz_PF84_0198f08a-3880-4871-b55e-4863ccf723d5 --webex-space Y2lzY29zcGFyazovL3VzL1JPT00vNTIxOWRiYTAtYWNiMC0xMWViLTgzYjctOTVlMTRhZTBhYTE3
```
Sample output: WebexTeams_Bot.jpg