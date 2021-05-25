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


# test result recording
test_status_string = ""
test_status = "None"
pass_counter = 0


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
        for device in genie_testbed.devices.values():

            try:
                device.connect(log_stdout=False)
                device_list.append(device)
                pass_counter += 1

            except errors.ConnectionError:
                # self.skipped(f"Failed to establish "f"connection to '{device.name}'")
                test_status_string = test_status_string + (
                    f"FAILED: Unable to establish " f"connection to '{device.name}'\n"
                )
                test_status = "Failed"

        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class Ping_NTP(aetest.Testcase):
    """
    Version Testcase - extract Serial numbers information from devices
    Verify that all SNs are covered by service contract (exist in contract_sn)
    """

    global test_status_string
    global test_status
    global pass_counter

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

        devices = self.parent.parameters["dev"]
        log.info(devices)
        aetest.loop.mark(self.ping_ntp, device=devices)

    @aetest.test
    def ping_ntp(self, device):
        """
        Verify that the OS version is correct
        """
        global test_status_string
        global test_status
        global pass_counter

        if device.os == "WIP":
            pass

        elif device.os == "ios":

            ntp_details = device.execute("show running-config | include ntp server")
            if ntp_details == "":
                # self.failed(f'NTP Server on {device} not found')
                test_status_string = (
                    test_status_string
                    + "FAILED: NTP Server on {} not found\n".format(device)
                )
                test_status = "Failed"
            ntp_detail_lines = ntp_details.splitlines()
            line_index = 0

            while line_index < len(ntp_detail_lines):

                ntp_server_ip = re.findall(
                    r"[0-9]+(?:\.[0-9]+){3}", ntp_detail_lines[line_index]
                )[0]
                try:
                    # store command result for later usage
                    result = device.ping(ntp_server_ip)

                except Exception as e:

                    match = re.search(r"(?P<success_rate_is>\d+) percent", str(e))
                    success_rate = match.group("success_rate_is")
                    test_status_string = (
                        test_status_string
                        + "FAILED: Ping NTP Server{} from device {} with success rate of {}%\n".format(
                            ntp_server_ip, device.name, success_rate
                        )
                    )
                    test_status = "Failed"
                    log.info(
                        "FAILED: Ping NTP Server{} from device {} with success rate of {}%".format(
                            ntp_server_ip, device.name, success_rate
                        )
                    )
                else:
                    # extract success rate from ping result with regular expression
                    match = re.search(r"(?P<success_rate_is>\d+) percent", result)
                    success_rate = match.group("success_rate_is")
                    if float(success_rate) > 0:
                        # ping responded
                        test_status_string = (
                            test_status_string
                            + "PASSED: Ping NTP Server {} from device {} with success rate of {}%\n".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )
                        pass_counter += 1
                        log.info(
                            "PASSED: Ping NTP Server {} from device {} with success rate of {}%".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )
                    else:
                        # packet loss was 100%
                        test_status = "Failed"
                        test_status_string = (
                            test_status_string
                            + "FAILED: Ping NTP Server {} from device {} with success rate of {}%\n".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )
                        log.info(
                            "FAILED: Ping NTP Server {} from device {} with success rate of {}%".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )
                line_index += 1

        elif device.os == "nxos":

            ntp_details = device.execute("show running-config | include ntp server")
            if ntp_details == "":
                # self.failed(f'NTP Server on {device} not found')
                test_status_string = (
                    test_status_string
                    + "FAILED: NTP Server on {} not found\n".format(device)
                )
                test_status = "Failed"
            ntp_detail_lines = ntp_details.splitlines()
            line_index = 0

            while line_index < len(ntp_detail_lines):

                ntp_server_ip = re.findall(
                    r"[0-9]+(?:\.[0-9]+){3}", ntp_detail_lines[line_index]
                )[0]
                try:
                    # store command result for later usage
                    result = device.ping(ntp_server_ip)

                except Exception as e:

                    match = re.search(
                        r"(?P<packet_loss_percent>\d+\.?\d+)% packet loss", str(e)
                    )
                    packet_loss = match.group("packet_loss_percent")
                    test_status_string = (
                        test_status_string
                        + "FAILED: Ping NTP Server{} from device {} with packet loss of {}%\n".format(
                            ntp_server_ip, device.name, packet_loss
                        )
                    )
                    test_status = "Failed"
                    log.info(
                        "FAILED: Ping NTP Server{} from device {} with packet loss of {}%".format(
                            ntp_server_ip, device.name, packet_loss
                        )
                    )
                else:
                    # extract success rate from ping result with regular expression
                    match = re.search(
                        r"(?P<packet_loss_percent>\d+\.?\d+)% packet loss", result
                    )
                    packet_loss = match.group("packet_loss_percent")
                    if float(packet_loss) < 100:
                        # ping responded
                        test_status_string = (
                            test_status_string
                            + "PASSED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )
                        pass_counter += 1
                        log.info(
                            "PASSED: Ping NTP Server {} from device {} with packet loss of {}%".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )
                    else:
                        # packet loss was 100%
                        test_status = "Failed"
                        test_status_string = (
                            test_status_string
                            + "FAILED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )
                        log.info(
                            "FAILED: Ping NTP Server {} from device {} with packet loss of {}%".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )
                line_index += 1
        else:
            test_status_string = (
                test_status_string
                + "FAILED: Device OS type {} not handled in script for device {}\n".format(
                    device.os, device
                )
            )
            test_status = "Failed"
            log.info(
                "FAILED: Device OS type {} not handled in script for device {}\n".format(
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
            self.failed(f"FAILED: Ping NTP Server Test\n{test_status_string}")
        if test_status == "None" and pass_counter == 0:
            self.failed(f"FAILED: Ping NTP anomaly, check script\n{test_status_string}")
        if test_status == "None" and pass_counter > 0:
            self.passed(f"PASSED: Ping NTP Server Test\n{test_status_string}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
