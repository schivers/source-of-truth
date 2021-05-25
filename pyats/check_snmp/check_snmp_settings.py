#!/usr/bin/env python3

# To get a logger for the script
import logging

from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handle errors with connections to devices
from unicon.core import errors

import pprint
import argparse
import re
from pyats.topology import loader

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO


# Test result recording
test_status_string = ""
test_status = "None"
pass_counter = 0

# Show run search commands to make it a little more generic and reusable, this takes a list form
show_run_include_commands = [
    "snmp-server community 7tzXPyiDZ82t RO",
    "snmp-server host 172.22.192.56 7tzXPyiDZ82t",
]

test_name = "Check SNMP Settings"


class MyCommonSetup(aetest.CommonSetup):
    """
    CommonSetup class to prepare for testcases
    Establishes connections to all devices in testbed
    """

    @aetest.subsection
    def establish_connections(self, testbed):
        """
        Establishes connections to all devices in testbed
        :param testbed:
        :return:
        """
        global test_status_string
        global test_status
        global pass_counter

        genie_testbed = Genie.init(testbed)
        self.parent.parameters["testbed"] = genie_testbed
        device_list = []
        test_status_string = test_status_string + (
            f"----START OF CONNECTION TESTS----\n"
        )
        for device in genie_testbed.devices.values():

            try:
                device.connect(log_stdout=False)
                device_list.append(device)
                test_status_string = test_status_string + (
                    f"PASSED: Establish " f"connection to '{device.name}'\n"
                )
                pass_counter += 1

            except errors.ConnectionError:
                # self.skipped(f"Failed to establish "f"connection to '{device.name}'")
                test_status_string = test_status_string + (
                    f"FAILED: Unable to establish " f"connection to '{device.name}'\n"
                )
                test_status = "Failed"

        # Pass list of devices to testcases
        test_status_string = test_status_string + (f"----END OF CONNECTION TESTS----\n")
        self.parent.parameters.update(dev=device_list)


class Check_DNS_Server_Settings(aetest.Testcase):

    global test_status_string
    global test_status
    global pass_counter
    # global ntp_server_ip_list
    global show_run_include_commands

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

        devices = self.parent.parameters["dev"]
        log.info(devices)
        aetest.loop.mark(self.check_dns_server_settings, device=devices)

    @aetest.test
    def check_dns_server_settings(self, device):
        """


        """

        global test_status_string
        global test_status
        global pass_counter
        test_status_string = test_status_string + "----START OF {} TESTS----\n".format(
            test_name
        )

        if device.os == "WIP":
            pass

        elif device.os == "nxos" or device.os == "ios":

            for show_run_include_command in show_run_include_commands:
                show_run_output = device.execute(
                    "show running-config | include " + show_run_include_command
                )
                if (
                    show_run_output != ""
                    and show_run_output.find(show_run_include_command) != -1
                ):
                    test_status_string = (
                        test_status_string
                        + 'PASSED: {} "{}" FOUND on {}\n'.format(
                            test_name, show_run_include_command, device
                        )
                    )
                    pass_counter += 1
                    log.info(
                        'PASSED: {} "{}" FOUND on {}'.format(
                            test_name, show_run_include_command, device
                        )
                    )
                else:
                    test_status_string = (
                        test_status_string
                        + 'FAILED: {} "{}" NOT CONFIGURED on {}\n'.format(
                            test_name, show_run_include_command, device
                        )
                    )
                    test_status = "Failed"
                    log.info(
                        'FAILED: {} "{}" NOT CONFIGURED on {}'.format(
                            test_name, show_run_include_command, device
                        )
                    )
        else:
            test_status_string = (
                test_status_string
                + "FAILED: Device OS type {} not handled in script for device {}\n".format(
                    device.os, device
                )
            )
            test_status = "Failed"
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
        #     pass

        global test_status_string
        global test_status
        global pass_counter

        if test_status == "Failed":
            self.failed(f"FAILED: {test_name}\n{test_status_string}")
        if test_status == "None" and pass_counter == 0:
            self.failed(
                f"FAILED: {test_name} anomaly, Nothing passed and it didnt fail either, check script\n{test_status_string}"
            )
        if test_status == "None" and pass_counter > 0:
            self.passed(f"PASSED: {test_name}\n{test_status_string}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
