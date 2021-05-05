from get_from_netbox import devices

from jinja2 import Template

print("Done imports")

#with open("templates/vlan_configuration.j2") as f:
#    vlan_template = Template(f.read())

print("Opening interface_configuration")
with open("templates/interface_configuration.j2") as f:
    interface_template = Template(f.read())


for device in devices:
    print("Device {} of role {}".format(device.name, device.device_role))

    config = "! Source of Truth Generated Configuration\n"

    # Layer 2 VLANs - Only for roles = ["Distribution", "Access"]
#    if device.device_role.name in ["Distribution", "Access"]:
#        print(" - Building L2 VLAN Configuration for Device")
#        config += vlan_template.render(vlans=vlans)

    # Interface Configurations
    if device.device_role.name in ["Distribution", "Access"]:
        print(" - Building Interface Configurations for Device")
        config += interface_template.render(interfaces=device.interfaces)

    # Generate Configuraiton File
    config_file_name = "/home/ntt/ftp/config-generator/{}.txt".format(device.name)
    with open(config_file_name, "w") as f:
        f.write(config)