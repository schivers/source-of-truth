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
from pyats.topology import loader

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO

# global variables
test_name = "Check CDP Enabled"

# interfaces:
interface_types_to_check_list = ["Ethernet", "mgmt"]


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
            testbed.connect(
                learn_hostname=True, log_stdout=False, connection_timeout=60
            )
        except (TimeoutError, StateMachineError, ConnectionError) as e:
            log.error("NOT CONNECTED TO ALL DEVICES")

    @aetest.subsection
    def verify_connected(self, testbed, steps):
        device_list = []

        d_name = []
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
            # ADD NEW TESTS CASES HERE
            aetest.loop.mark(CDP_Enabled, device=device_list, uids=d_name)

        else:
            self.failed()


class CDP_Enabled(aetest.Testcase):
    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def cdp_enabled(self, device):
        """
        Verify that the OS version is correct
        """
        if device.os == "ios" or device.os == "iosxe":
            all_interfaces_cdp_enabled = True
            cdp_interface_detail_string = ''
            out = device.parse("show interfaces")
            for interface in out.items():
                for interfaces_types_to_check in interface_types_to_check_list:
                    if interface[0].find(interfaces_types_to_check) != -1:
                        
                        
                        interface_detail = device.execute(
                            "show cdp interface " + interface[0]
                        )
                        interface_detail_line_array = interface_detail.splitlines()
                        line_index = 0
                        cdp_enabled = False
                        while line_index < len(interface_detail_line_array):
                            if (
                                interface_detail_line_array[line_index].find(
                                    "Sending CDP packets"
                                )
                                != -1
                            ):
                                cdp_enabled = True
                            line_index += 1
                        if cdp_enabled:
                            cdp_interface_detail_string = cdp_interface_detail_string + "PASSED: cdp enabled {} on {}\n".format(interface[0], device)
                            log.info(
                                "PASSED: cdp enabled {} on {}".format(
                                    interface[0], device
                                )
                            )
                        else:
                            all_interfaces_cdp_enabled = False
                            cdp_interface_detail_string = cdp_interface_detail_string + "FAILED: cdp not enabled {} on {}\n".format(interface[0], device)                                
                            log.info(
                                "FAILED: cdp not enabled {} on {}".format(
                                    interface[0], device
                                )
                            )
            if all_interfaces_cdp_enabled:
                self.passed(cdp_interface_detail_string)
            else:
                self.failed(cdp_interface_detail_string)

        else:

            self.failed(
                "FAILED: Device OS type {} not handled in script for device {}".format(
                    device.os, device
                )
            )
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
