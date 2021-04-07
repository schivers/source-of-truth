# Netbox as a Source of Truth
This projects seeks to use Netbox to document the Baku stadium network for EURO2020 (held in 2021).

![Netbox Top Level](screens/Netbox-main.jpg)

**Why use Netbox?**
While the initial population of Netbox can be a big task the benefits of having a single source of truth and point of update are undenyable especially in a rapidly changing environment
like the EURO's. The time consuming element was the population of Interface configuration which was largley manual. I will look to automate this in the future.

Netbox provides the Baku team with 
- Dynamically generated topology diagrams (no more Visio to update)
- Patching schedules (no more excel)
- Rack layouts (no more visio)
- Attach site plans to IDF locations for quick reference (no need to locate latest diagrams)
- IP Address Management
- An API interface that allows netbox to be used as a dynamic inventory
  - Generate configs
  - Backup active devices
  - Check live interfaces for errors
  - Push config changes from Netbox to devices

The following Netbox objects are populated
- **Site.** Used to record the site name and location. Baku and IBC are defined. IBC just because Baku has WAN links that connect to routers in the IBC.
- **Racks.** Eqipment rack identifiers (e.g IDF-G-A)
- **Tenants.** UEFA
- **Tags.** Used to label the zone that the device is installed into. UEFA defines zones (e.g. UEFA Org. Office (1.1)) and defines the connectivity requirement for each zone. 
- **Devices.** All devices; Core, Distribution and Access Switches, Unmanaged Switches, 
- **Device Roles.** Role example are 'Access' for 2960 access switching, 'Distribution' for the TVC 3650 distribution switch and 'Core' for the 9500 core switches. 
- **Platforms.** Records the operating system. Note that 'IOS' is used in most instances even though the core is runnign IOS-XE. IOS-XE is not a supported type by some plugins. 
- **Virtual Chassis.** Allow's a primary switch to be nominated for a Virtual Chassis/Stack. All interfaces are viewable from that primary switch in Netbox. 
- **Device types.** Defines the interfaces for each model/SKU of device
- **Manufacturers.** Cisco, Meraki etc
- **Cables.** Cables are dynamically created when two interfaces are connected in Netbox. Cables are labeled in Netbox using the patch panel/port ID
- **Interfaces.** Device physical and logical interface configuration
- **IP Addresses.** IP addressing allocations
- **Prefixes.** Site prefix allocations
- **Aggregates.** Site IP aggregates
- **VRF's.** Site VRF's
- **Route Targets.** Site Route Target
- **VLANs.** Site VLAN Database
- **VLAN Groups.** Used to record VLAN allocations per VRF. A VLAN Group is defined for each VRF.

## Sub projects
- **Push config** - When an interface VLAN (access ports only) is changed in Netbox push the config automatically to the switch.
- **Topology Viewer** - Dynamically generate topology diagrams
- **Config Generator** - Generate Interface Configuration files for all devices in Netbox
- **Testing** - Use PyATS to test the deployed network
    - PyATS filters devices to include only devices with an 'active' status from Netbox
    - **Learn device status** for comparison. e.g. compare network state today with yesterday - tell me what changed.
    - Check for **interface errors**
- **Config Backup** - Use Ansible to backup configs from active devices
- ** FTP server** - FTP server running on the host so that all **generated** and **backed up** config files may be accessed via FTP 
    
## Deployed Packages
- Netbox docker (2.10.5) - https://github.com/netbox-community/netbox-docker
- Topology viewer Netbox plugin - https://github.com/iDebugAll/nextbox-ui-plugin
- Webhooks - https://github.com/adnanh/webhook
- Nornir (3.1.0) - https://nornir.readthedocs.io/en/latest/
- PYATS (21.2) - https://developer.cisco.com/docs/pyats/
- Ansible (3.1.0) - https://docs.ansible.com/
 

## Push Config
Netbox is configured to generate a weebhook post when there is a change in Netbox to the 'interface' page. A trigger filter ensures that the webhook is triggered only
if an interface is configured as an access port. This stops an unplink (trunk) from being reconfigured but the downside is that it cannot currently be used for AccessPoint
ports. I may develop this further to allow this as the port mode in Netbox does distinguish between the 'tagged (all)' used for uplinks in my config and the 'tagged' for AccessPoints. 
A webhook server (listener) is running on the same bare metal server as Netbox docker and uses some scripting to push the config via Netmiko, Napalm and Nornir to the device.

Reference - https://journey2theccie.wordpress.com/2020/04/07/automating-my-ccie-lab-pt-4-netmiko-napalm-nornir/

## Topology Viewer
This is a user interface plugin for Netbox that provides a dynamically generated topology. The generated topology is draggable and can be saved for future recall. 
Replaces static Visio diagrams and removes the need to keep diagrams updated with change as they are dynamically generated using the Netbox connectivity data.

The following link has the install instructions
Reference - https://github.com/iDebugAll/nextbox-ui-plugin

## Config Generator (Interfaces)
The config generator is a modified script from Hank Preston (Cisco). The script generates a config for each device using the Netbox interface configuration as the source of truth.

Reference - https://github.com/hpreston/netdevops_demos/tree/master/source-of-truth

To use
```
cd ~/netdevops_demos/source-of-truth
source src_env
python3 build_configs.py
```

Configs are written to /home/ntt/ftp/config-generator

Note that as there are >500 devices defined in Netbox this script will take a quite a few minutes to complete. 

## Testing (PyATS)

## Switch Config Generator (Basic system config)
This uses Ansible to generate the switch config including uplinks using an Ansible playbook and a csv for the source data. I used this before I started using Netbox else I would have used Netbox.


## Config Backup (Ansible)
This script uses an Ansible playbook to simply backup the config of the devices marked with an 'active' status in Netbox.

Ansible uses Vault to store the device username and password credentials

Run with
```
cd /home/ntt/ansible
sudo ansible-playbook cisco-backup.yaml -i nb_inventory.yml --ask-vault-pass
```

Configs are backed up to 
/home/ntt/ftp/backups

## FTP Server (VSFTP)
A single FTP account is created (ntt) to allow engineers access to the generated and the backed up config files.

```
ntt@inspiron-3521:~/ftp$ ll
total 16
dr-xr-xr-x  4 nobody nogroup 4096 Apr  6 19:15 ./
drwxr-xr-x 27 ntt    ntt     4096 Apr  6 19:00 ../
drwxr-xr-x  2 ntt    ntt     4096 Apr  6 19:13 backups/
drwxr-xr-x  2 ntt    ntt     4096 Apr  6 19:15 config-generator/
```

Reference 
- https://www.techrepublic.com/article/how-to-quickly-setup-an-ftp-server-on-ubuntu-18-04/
- https://www.digitalocean.com/community/tutorials/how-to-set-up-vsftpd-for-a-user-s-directory-on-ubuntu-16-04

