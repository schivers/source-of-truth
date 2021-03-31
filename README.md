# Netbox as a Source of Truth
This projects seeks to use Netbox to document the Baku stadium network for EURO2020 (held in 2021). Netbox API can then be used as the information source to program the network.

The following Netbox objects are populated
- **Organization.** UEFA
- **Site.** Baku, IBC
- **Racks.** Eqipment rack identifiers (e.g IDF-G-A)
- **Tenants.** UEFA
- **Tags.** Used to label the zone that the device is installed into. UEFA defines zones (e.g. UEFA Org. Office (1.1)) and defines the connectivity requirement for each zone. 
- **Devices.**
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
- When an interface VLAN (access ports only) is changed in Netbox push the config automatically to the switch.
- Dynamically generate topology diagrams
- Generate Interface Configuration files for all devices in Netbox
- Use PyATS to test the deployed network
    - PyATS filters devices to include only devices with an 'active' status from Netbox
    - Learn device status for comparison. e.g. compare network state today with yesterday - tell me what changed.
    - Check for interface errors
    
## Deployed Libraries
- Netbox docker
- Webhooks - https://github.com/adnanh/webhook
- Nornir (3.1.0) - https://nornir.readthedocs.io/en/latest/
- PYATS (21.2)
- Ansible (3.1.0)