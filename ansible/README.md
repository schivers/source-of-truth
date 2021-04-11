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
4. Update the switch boot variable to point at the new IOS image
5. Reload the switch
6. Use the wait_for module to wait 90 sec before starting to try and connect to the device on tcp22 (SSH). 
7. Run the ios_facts module again to verify the switch has been upgraded to the correct version


Configure the core 9500 switch as an SCP server
```
ip scp server enable
```

Confirm that the inventory is working
```
ansible-inventory -v --list -i nb_inventory.yaml
```

Perform a dry run to see which devices will be upgraded
```
sudo ansible-playbook -i nb_inventory.yaml switch_upgrade_check.yaml --ask-vault-pass
```

Run the full upgrade playbook
```
sudo ansible-playbook -i nb_inventory.yaml switch_upgrade.yaml --ask-vault-pass
```



**Backup the config of all devices with status = 'active'**

This playbook simply pulls the devices marked with an active status from Netbox and backs up the config from each to ~/ftp/backups
```
ntt@inspiron-3521:~/ansible$ sudo ansible-playbook cisco-backup.yaml -i nb_inventory.yml --ask-vault-pass
```



**Push out a config update**
This playbook will use the filtered Netbox inventory to push out a config update to all davices returned by Netbox. the example playbook enables the SCP server and revised access-list 11.
```
sudo ansible-playbook config_update_v105b.yaml -i nb_inventory.yaml --ask-vault-pass
```
