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
import re
from pyats.topology import loader

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO


# test result recording
test_status_string = ""
test_status = "None"
pass_counter = 0


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
            aetest.loop.mark(Check_LLDP, device=device_list,uids=d_name)           
        else:
            self.failed()



class Check_LLDP(aetest.Testcase):
    """
    Version Testcase - extract LLDP config from devices
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """
        pass

    @aetest.test
    def check_lldp(self, device):
        if device.os == "ios" or device.os == "iosxe" or device.os == "iosxr" or device.os == "nxos":

            test = device.api.verify_lldp_in_state(device)
            if test:
                self.passed('lldp is enabled on device {}'.format(device))
            else:
                self.failed('lldp is not enabled on device {}'.format(device))

        else:
            self.failed("FAILED: Device OS type {} not handled in script for device {}".format(device.os, device))
            log.info(
                "FAILED: Device OS type {} not handled in script for device {}".format(
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
