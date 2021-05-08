# Baku ICT Staff User Guide

## Netbox
Add a browser shortcut to http://192.168.1.191:8000/dcim/sites/baku/

As well as the usual Netbox links, notice the light blue links (top right) which are shortcuts to various systems we are using to manage the stadium ICT.

## Build and Configuration
We are using Netbox as our source of truth and therefore all config is applied first to netbox. We then can use an Ansible script to pull the configuration from Netbox and generate interface configuration files.

View the last generated config files
http://192.168.1.191:8002/config-generator/

## Testing
We are using PyATS to automate a lot of repetative testing. 

View the test report files
http://192.168.1.191:8088
