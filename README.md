# Netbox as a Source of Truth
This projects seeks to use Netbox to document the Baku stadium network for EURO2020 (held in 2021). Netbox API can then be used as the information source to program the network.

The following Netbox objects are populated
- **Site.** Baku, IBC
- **Racks.** Eqipment rack identifiers (e.g IDF-G-A)
- **Tenants.** UEFA
- **Tags.** Used to label the zone that the device is installed into. UEFA defines zones (e.g. UEFA Org. Office (1.1)) and defines the connectivity requirement for each zone. 
- **Devices.** All devices; Core, Distribution and Access Switches, Unmanaged Switches, 
- **Device Roles.**
- **Platforms.**
- **Virtual Chassis.**
- **Device types.**
- **Manufacturers.**
- **Cables.**
- **Interfaces.**
- **IP Addresses.**
- **Prefixes.**
- **Aggregates.**
- **VRF's.**
- **Route Targets.**
- **VLANs.**
- **VLAN Groups.**

## Sub projects
- **Push config** - When an interface VLAN (access ports only) is changed in Netbox push the config automatically to the switch.
- **Topology Viewer** - Dynamically generate topology diagrams
- **Config Generator** - Generate Interface Configuration files for all devices in Netbox
- **Testing** - Use PyATS to test the deployed network
    - PyATS filters devices to include only devices with an 'active' status from Netbox
    - **Learn device status** for comparison. e.g. compare network state today with yesterday - tell me what changed.
    - Check for **interface errors**
- **Config Backup** - Use Ansible to backup configs from active devices
    
## Deployed Packages
- Netbox docker - https://github.com/netbox-community/netbox-docker
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

## Testing (PyATS)

## Switch Config Generator (Basic system config)
This uses Ansible to generate the switch config including uplinks using an Ansible playbook and a csv for the source data. I used this before I started using Netbox else I would have used Netbox.


## Config Backup (Ansible)