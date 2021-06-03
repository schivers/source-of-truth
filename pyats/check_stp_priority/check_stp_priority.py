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

import argparse
import re
from pyats.topology import loader
import pprint

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO

#device types and STP commands to check
access_switch = ['Catalyst WS-C2960L-24PS-LL','Catalyst WS-C2960L-48PS-LL'] #list of access switches
access_switch_config = 'spanning-tree vlan 1-4094 priority 24576' #what to look for in show running-config if its an access switch
distribution_switch = ['WS-C3650-12X48UR'] #like above, This might need the word 'Catalyst in there'
distribution_switch_config = 'spanning-tree vlan 1-4093 priority 8192'
core_switch = ['tbc'] #for Shaun to complete
core_switch_config = 'tbc'

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
            aetest.loop.mark(Check_STP_Priority, device=device_list,uids=d_name)
            
        else:
            self.failed()


class Check_STP_Priority(aetest.Testcase):

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def check_stp_priority(self, device):
        """
        Verify that the STP Priority is correct
        """
        config_to_find = ''
        if device.os == 'ios' or device.os == 'iosxe':
            try:
                out = device.parse("show running-config")
                
            except Exception as e:
                self.failed('Exception occured '.format(str(e)))
            else:
                if device.type in access_switch:
                    config_to_find = access_switch_config
                elif device.type in distribution_switch:
                    config_to_find = distribution_switch_config
                elif device.type in core_switch:
                    config_to_find = core_switch_config
                else:
                    self.failed('Unknown device type "{}" on device "{}"'.format(device.type,device))
                
                if config_to_find in out:
                    self.passed('Config "{}" was found on device {}'.format(config_to_find,device))
                else:
                    self.failed('Config "{}" not found on device {}'.format(config_to_find,device))
        else:
            self.failed("FAILED: Device OS type {} not handled in script for {}".format(device.os, device))
            log.info(
                "FAILED: Device OS type {} not handled in script for {}".format(
                    device.os, device
                )
            )


class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """

    # uncomment to add new subsections
    @aetest.subsection
    def subsection_cleanup_one(self):
        pass

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
