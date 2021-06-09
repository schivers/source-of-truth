#!/usr/bin/env python3

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handle errors with connections to devices
from unicon.core import errors
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

import pprint
import argparse
from pyats.topology import loader

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO

# Software versions:
iosxe_os = ["16.12.5"]
ios_os = ["15.2(7)E3"]
nxos_os = ["9.3(9)"]

#software version dictionary, just copy the key value pairs below to add more device types and versions.
software_version_dictionary = {
    "Catalyst 9500-40X":"16.12.4",
    "Catalyst WS-C2960L-24PS-LL":"15.2(7)E3",
    "Catalyst WS-C2960L-48PS-LL":"15.2(7)E3",
    "WS-C3650-12X48UR":"16.09.06",
    "ASR1001-HX":"16.12.5"
    }

class MyCommonSetup(aetest.CommonSetup):

    @aetest.subsection
    def establish_connections(self, testbed):
        """
        Establishes connections to all devices in testbed
        :param testbed:
        :return:
        """

        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        try:
            testbed.connect(log_stdout=False)
        except (TimeoutError, StateMachineError, ConnectionError) as e:
            log.error("NOT CONNECTED TO ALL DEVICES")
            

    @aetest.subsection
    def verify_connected(self, testbed, steps): 
        device_list = []
        d_name=[]
        for device_name, device in testbed.devices.items():

            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                log.info(device)
                if device.connected:
                    log.info(f"{device_name} connected status: {device.connected}")
                    device_list.append(device)
                    d_name.append(device_name)
                else:
                    log.error(f"{device_name} connected status: {device.connected}")
                    step.skipped()
                    
        # Pass list of devices to testcases
        if device_list:
            #ADD NEW TESTS CASES HERE
            aetest.loop.mark(Check_Version_By_Type, device=device_list,uids=d_name)
            
        else:
            self.failed()

class Check_Version_By_Type(aetest.Testcase):
    """
    Version Testcase - extract Serial numbers information from devices
    Verify that all SNs are covered by service contract (exist in contract_sn)
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def check_version_by_type(self, device):
        """
        Verify that the OS version is correct
        """

        try:
            out = device.parse("show version")

        except Exception as e:
            self.failed('Exception occured '.format(str(e)))
        else:
            if device.type in software_version_dictionary:
                if software_version_dictionary[device.type] == out["version"]["version"]:
                    #log.info('software version from dictionary is {} and version on device is {}'.format(software_version_dictionary[device.type],out["version"]["version"]))
                    self.passed('Software version for {} should be {} and version on device is {}'.format(device.type,software_version_dictionary[device.type],out["version"]["version"]))
                else:
                    self.failed('Software version for {} should be {} and version on device is {}'.format(device.type,software_version_dictionary[device.type],out["version"]["version"]))
                    #log.info('software version from dictionary is {} and version on device is {}'.format(software_version_dictionary[device.type],out["version"]["version"]))
            else:
                self.failed('device type {} not found in dictionary for device {}, update script to include this'.format(device.type, device.name))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
