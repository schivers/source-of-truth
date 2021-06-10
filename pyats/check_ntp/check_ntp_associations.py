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

# Central NTP server details
ntp_server_ip_list = ["172.22.192.56", "10.224.0.100"]


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
            aetest.loop.mark(Check_NTP_Associations, device=device_list, uids=d_name)

        else:
            self.failed()


class Check_NTP_Associations(aetest.Testcase):

    global ntp_server_ip_list

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def check_ntp_associations(self, device):
        """
        Ping central NTP server
        """

        if device.os == "WIP":
            pass

        elif device.os == "nxos" or device.os == "iosxe" or device.os == "ios":

            ntp_details = device.execute("show running-config | include ntp server")
            if ntp_details == "":
                # self.failed(f'NTP Server on {device} not found')
                # test_status_string = (
                #    test_status_string
                #    + "FAILED: No NTP Servers configured on {}\n".format(device)
                # )
                # test_status = "Failed"
                self.failed("FAILED: No NTP Servers configured on {}".format(device))
                log.info("FAILED: No NTP Servers configured on {}".format(device))
            else:
                # check the NTP servers are listed
                ntp_server_count = 0
                for ntp_server_ip in ntp_server_ip_list:
                    if ntp_details.find(ntp_server_ip) == -1:
                        # ntp server not found
                        # test_status_string = (
                        #    test_status_string
                        #    + "FAILED: NTP Server {} not configured on {}\n".format(
                        #        ntp_server_ip, device
                        #    )
                        # )
                        # test_status = "Failed"
                        self.failed(
                            "FAILED: NTP Server {} not configured on {}".format(
                                ntp_server_ip, device
                            )
                        )
                        log.info(
                            "FAILED: NTP Server {} not configured on {}".format(
                                ntp_server_ip, device
                            )
                        )
                    else:
                        # ntp server found
                        # test_status_string = (
                        #    test_status_string
                        #    + "PASSED: NTP Server {} configured on {}\n".format(
                        #    )
                        # )
                        #        ntp_server_ip, device
                        # ntp_server_count += 1
                        # pass_counter += 1
                        self.passed(
                            "PASSED: NTP Server {} configured on {}".format(
                                ntp_server_ip, device
                            )
                        )
                        log.info(
                            "PASSED: NTP Server {} configured on {}".format(
                                ntp_server_ip, device
                            )
                        )

                if ntp_server_count == len(ntp_server_ip_list):
                    # All required NTP Servers Listed, check NTP Associations on this device.
                    ntp_details = device.execute("show ntp status")

                    if ntp_details.find("Clock is synchronized") == -1:
                        # test_status_string = (
                        #    test_status_string
                        #    + "FAILED: NTP unsynchronised on {}\n".format(device)
                        # )
                        # test_status = "Failed"
                        self.failed("FAILED: NTP unsynchronised on {}".format(device))
                        log.info("FAILED: NTP unsynchronised on {}".format(device))
                    else:
                        # test_status_string = (
                        #    test_status_string
                        #    + "PASSED: NTP synchronised on {}\n".format(device)
                        # )
                        # pass_counter += 1
                        self.passed("PASSED: NTP synchronised on {}".format(device))
                        log.info("PASSED: NTP synchronised on {}".format(device))
        else:
            # test_status_string = (
            #    test_status_string
            #    + "FAILED: Device OS type {} not handled in script for device {}\n".format(
            #        device.os, device
            #    )
            # )
            # test_status = "Failed"
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
        #     pass
        """
        global test_status_string
        global test_status
        global pass_counter

        if test_status == "Failed":
            self.failed(f"FAILED: Check NTP Associations\n{test_status_string}")
        if test_status == "None" and pass_counter == 0:
            self.failed(
                f"FAILED: Check NTP Associations anomaly, Nothing passed and it didnt fail either, check script\n{test_status_string}"
            )
        if test_status == "None" and pass_counter > 0:
            self.passed(f"PASSED: Check NTP Associations\n{test_status_string}")
        """


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
