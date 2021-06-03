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
            aetest.loop.mark(Ping_Default_GW, device=device_list,uids=d_name)
            
        else:
            self.failed()


class Ping_Default_GW(aetest.Testcase):

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def ping_default_gw(self, device):
        """
        Verify that the default gateway is correct and can be pinged.
        """

        if device.os == 'ios' or device.os == 'iosxe':

            out_details = device.execute('show ip route')
            if out_details == '':
                self.failed("FAILED: default route on {} not found".format(device))
            out_detail_lines = out_details.splitlines()
            line_index = 0
            found_default_gateway = False
            while line_index < len(out_detail_lines):
                if device.os == 'ios':
                    match = re.search(r"Default gateway is (?P<default_gateway>[0-9]+(?:\.[0-9]+){3})", out_detail_lines[line_index])
                if device.os == 'iosxe':
                    match = re.search(r"Gateway of last resort is (?P<default_gateway>[0-9]+(?:\.[0-9]+){3})", out_detail_lines[line_index])
           
                if match != None:
                    default_gateway = match.group("default_gateway")
                    found_default_gateway = True

                    try:
                        # store command result for later usage
                        result = device.ping(default_gateway)

                    except Exception as e:

                        match = re.search(r"(?P<success_rate_is>\d+) percent", str(e))
                        success_rate = match.group("success_rate_is")
                        self.failed("FAILED: Ping default gateway {} from device {} with success rate of {}%".format(default_gateway, device.name, success_rate))
                        log.info(
                            "FAILED: Ping default gateway {} from device {} with success rate of {}%".format(
                                default_gateway, device.name, success_rate
                            )
                        )
                    else:
                        # extract success rate from ping result with regular expression
                        match = re.search(r"(?P<success_rate_is>\d+) percent", result)
                        success_rate = match.group("success_rate_is")
                        if float(success_rate) > 0:
                            # ping responded
                            self.passed("PASSED: Ping default gateway {} from device {} with success rate of {}%".format(default_gateway, device.name, success_rate))
                            log.info(
                                "PASSED: Ping default gateway {} from device {} with success rate of {}%".format(
                                    default_gateway, device.name, success_rate
                                )
                            )
                        else:
                            # packet loss was 100%
                            self.failed("FAILED: Ping default gateway {} from device {} with success rate of {}%".format(default_gateway, device.name, success_rate))
                            log.info(
                                "FAILED: Ping default gateway {} from device {} with success rate of {}%".format(
                                    default_gateway, device.name, success_rate
                                )
                            )
                line_index += 1

            if not found_default_gateway:
                self.failed("FAILED: Default gateway on device {} not found".format(device.name))
                log.info("FAILED: Default gateway on device {} not found".format(device.name))
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
