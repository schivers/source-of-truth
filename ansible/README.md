Ansible requires an inventory to run against and we can use this to be selective (filter) which inventory items we feen into Ansible. The inventory file ia in YAML format and defines
how Ansible accesses Netbox (URL and Token) and contains an optional grouping and filiter section.

The following will return a JSON formatted output of all devices in Netbox with the status 'active'. The returned output will group devices by device_roles and platforms.
```
---
plugin: netbox
api_endpoint: http://192.168.1.191:8000/
token: '0123456789abcdef0123456789abcdef01234567'
validate_certs: false
config_context: true
group_by:
 - device_roles
 - platforms
compose:
 ansible_network_os: platform.slug
query_filters:
 - has_primary_ip: True
 - status: "active"
 ```

Example inventory files

| Filename | Purpose |
| ------ | ------ |
| nb_inventory.yaml | Use to return all devices with a state = active |
| nb_inv_upgrade.yaml | Used to return devices that require a code upgrade. The device state in Netbox is set to "staged" and then the Ansible "switch_upgrade.yaml" playbook is run using the nb_inv_upgrade.yaml to upgrade the device | 

**Upgrade switches**
This playbook will gather facts for each device in the inventory file and compare the learnt IOS version against the version defined in the playbook. The inventory file used in my example returns all devices will and active status.
I use the core Catalyst 9500 as the SCP server

Playbook steps
1. Gather facts for each device returned from the Netbox inventory and compare the learnt IOS version to the required version. the Task debug will print a list of those switches that require an upgrade.
2. Create a dated folder and backup the device running-configs
3. Copy the IOS image to the switch. **Note that the script assumes there is sufficient space on the flash**


Configure the core 9500 switch as an SCP server
``
ip scp server enable
```


Confirm that the inventory is working
```
ansible-inventory -v --list -i nb_inventory.yaml
```

Perform a dry run to see which devices will be upgraded
``
sudo ansible-playbook -i nb_inv_upgrade.yaml switch_upgrade_check.yaml --ask-vault-pass
``

Run the full upgrade playbook
```
sudo ansible-playbook -i nb_inv_upgrade.yaml switch_upgrade.yaml --ask-vault-pass
```

**Config Backup of all devices with status = 'active'**
Sample run
```
ntt@inspiron-3521:~/ansible$ sudo ansible-playbook cisco-backup.yaml -i nb_inventory.yml --ask-vault-pass
Vault password:

PLAY [Backup all network ios switches] *************************************************************************************************************************************************************
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts

TASK [Gathering Facts] *****************************************************************************************************************************************************************************
ok: [BAKMTR1SWA01]
[WARNING]: Ignoring timeout(10) for ios_facts
ok: [BAKMTR1SWA02]
ok: [BAKMTR2SWA01]
ok: [BAKMTR2SWA02]
ok: [BAKMTR1SWC02]
ok: [BAKMTR1SWC01]

TASK [show run] ************************************************************************************************************************************************************************************
ok: [BAKMTR2SWA01]
ok: [BAKMTR1SWA01]
ok: [BAKMTR1SWC02]
ok: [BAKMTR1SWA02]
ok: [BAKMTR1SWC01]
ok: [BAKMTR2SWA02]

TASK [save output to /opt/ansible/backups] *********************************************************************************************************************************************************
changed: [BAKMTR2SWA01]
changed: [BAKMTR1SWA02]
changed: [BAKMTR1SWA01]
changed: [BAKMTR1SWC01]
changed: [BAKMTR1SWC02]
changed: [BAKMTR2SWA02]

PLAY RECAP *****************************************************************************************************************************************************************************************
BAKMTR1SWA01               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR1SWA02               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR1SWC01               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR1SWC02               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR2SWA01               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR2SWA02               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
```

```
ntt@inspiron-3521:~/ansible$ cd /opt/ansible/backups/
ntt@inspiron-3521:/opt/ansible/backups$ ll
total 400
drwxr-xr-x 2 root root  4096 Apr  6 12:08 ./
drwxr-xr-x 3 root root  4096 Mar  3 15:24 ../
-rw-r--r-- 1 root root 10387 Mar  3 18:53 BAKMTR1SWA01_20210303-1853.txt
-rw-r--r-- 1 root root  8045 Mar  3 19:18 BAKMTR1SWA01_20210303-1918.txt
-rw-r--r-- 1 root root  8045 Mar  4 11:04 BAKMTR1SWA01_20210304-1103.txt
-rw-r--r-- 1 root root  8045 Mar  4 11:10 BAKMTR1SWA01_20210304-1110.txt
-rw-r--r-- 1 root root  8345 Apr  6 11:52 BAKMTR1SWA01_20210406-1152.txt
-rw-r--r-- 1 root root  8345 Apr  6 11:56 BAKMTR1SWA01_20210406-1156.txt
-rw-r--r-- 1 root root  8345 Apr  6 12:08 BAKMTR1SWA01_20210406-1208.txt
-rw-r--r-- 1 root root 10387 Mar  3 19:18 BAKMTR1SWA02_20210303-1918.txt
-rw-r--r-- 1 root root 10387 Mar  4 11:04 BAKMTR1SWA02_20210304-1103.txt
-rw-r--r-- 1 root root 10387 Mar  4 11:10 BAKMTR1SWA02_20210304-1110.txt
-rw-r--r-- 1 root root 10314 Apr  6 11:52 BAKMTR1SWA02_20210406-1152.txt
-rw-r--r-- 1 root root 10314 Apr  6 11:56 BAKMTR1SWA02_20210406-1156.txt
-rw-r--r-- 1 root root 10314 Apr  6 12:08 BAKMTR1SWA02_20210406-1208.txt
-rw-r--r-- 1 root root 54587 Mar  4 11:10 BAKMTR1SWC01_20210304-1110.txt
-rw-r--r-- 1 root root 60903 Apr  6 12:08 BAKMTR1SWC01_20210406-1208.txt
-rw-r--r-- 1 root root 27418 Apr  6 11:52 BAKMTR1SWC02_20210406-1152.txt
-rw-r--r-- 1 root root 27418 Apr  6 11:56 BAKMTR1SWC02_20210406-1156.txt
-rw-r--r-- 1 root root 27418 Apr  6 12:08 BAKMTR1SWC02_20210406-1208.txt
-rw-r--r-- 1 root root  7783 Apr  6 11:52 BAKMTR2SWA01_20210406-1152.txt
-rw-r--r-- 1 root root  7783 Apr  6 11:56 BAKMTR2SWA01_20210406-1156.txt
-rw-r--r-- 1 root root  7783 Apr  6 12:08 BAKMTR2SWA01_20210406-1208.txt
-rw-r--r-- 1 root root  7835 Apr  6 11:52 BAKMTR2SWA02_20210406-1152.txt
-rw-r--r-- 1 root root  7835 Apr  6 11:56 BAKMTR2SWA02_20210406-1156.txt
-rw-r--r-- 1 root root  7835 Apr  6 12:08 BAKMTR2SWA02_20210406-1208.txt
```