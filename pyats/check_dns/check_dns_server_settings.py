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


# Test result recording
test_status_string = ""
test_status = "None"
pass_counter = 0

# Show run search commands to make it a little more generic and reusable
show_run_include_commands = [
    "ip name-server 10.224.0.100",
    "no ip domain-lookup",
    "ip domain-name uefa.local",
]

test_name = "Check DNS Server Settings"


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
            aetest.loop.mark(Check_DNS_Server_Settings, device=device_list, uids=d_name)

        else:
            self.failed()


class Check_DNS_Server_Settings(aetest.Testcase):

    # global ntp_server_ip_list
    global show_run_include_commands

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def check_dns_server_settings(self, device):

        test_status_string = ""
        test_passed = True
        if device.os == "nxos" or device.os == "ios" or device.os == "iosxe":
            for show_run_include_command in show_run_include_commands:
                if device.os == "nxos":
                    show_run_output = device.execute(
                        'show running-config | include "'
                        + show_run_include_command
                        + '"'
                    )
                else:
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
                    test_passed = False
                    log.info(
                        'FAILED: {} "{}" NOT CONFIGURED on {}'.format(
                            test_name, show_run_include_command, device
                        )
                    )
            if test_passed:
                self.passed(test_status_string)
            else:
                self.failed(test_status_string)

        else:
            self.failed(
                "FAILED: Device OS type {} not handled in script for {}".format(
                    device.os, device
                )
            )
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
