#PyATS - Python Automated Test Scripts
PyATS uses a testbed file that describes the test environment. Netbox can be used as the source to generate a testbed file and a filter can be used to refine the device list returned by Netbox.
The query filter is simply the URI that appears after the '&' wehn using the search function in the Netbox GUI.

First we need to set up the environment variables. I have save these into src_env so all we need to do is 'source' the variables
```
cd ~/
source src_env
```

Now we can create the testbed.yaml file. The following example will create a testbed.yaml containing all devices with a role of access, distribution or core and includes the topology connections.
```
cd pyats
pyats create testbed netbox --output testbed.yaml --netbox-url=${NETBOX_URL} --user-token=${NETBOX_TOKEN} --def_user=admin --def_pass=3uro2o2o --url_filter='q=&status=active&role=access&role=core&role=distribution&mac_address=&has_primary_ip=&local_context_data=&virtual_chassis_member=&console_ports=&console_server_ports=&power_ports=&power_outlets=&interfaces=&pass_through_ports=' --topology
```

## Device State
PyATS can be used to capture the device state. The following learns the state of all devices in the testbed and saves the information in /learn 
```
genie learn all --testbed-file testbed.yaml --output learn
```

## Check Interfaces for errors
```
easypy checkerrors_job.py -html_logs SAThtml -no_archive -testbed_file testbed.yaml
```
