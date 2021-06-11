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

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO

# Central NTP server details - This is a list, more ip addresses can be added and will be iterated.
ntp_server_ip_list = ["10.224.0.100"]


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
            aetest.loop.mark(Ping_Central_NTP, device=device_list, uids=d_name)

        else:
            self.failed()


class Ping_Central_NTP(aetest.Testcase):

    global ntp_server_ip_list

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def ping_central_ntp(self, device):
        """
        Ping central NTP server
        """

        if device.os == "WIP":
            pass

        elif device.os == "nxos":
            for ntp_server_ip in ntp_server_ip_list:
                try:
                    # store command result for later usage
                    result = device.ping(ntp_server_ip)

                except Exception as e:

                    match = re.search(
                        r"(?P<packet_loss_percent>\d+\.?\d+)% packet loss", str(e)
                    )
                    packet_loss = match.group("packet_loss_percent")
                    self.failed(
                        "FAILED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
                            ntp_server_ip, device.name, packet_loss
                        )
                    )
                    log.info(
                        "FAILED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
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
                        self.passed(
                            "PASSED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )
                        log.info(
                            "PASSED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )
                    else:
                        self.failed(
                            "FAILED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )
                        log.info(
                            "FAILED: Ping NTP Server {} from device {} with packet loss of {}%\n".format(
                                ntp_server_ip, device.name, packet_loss
                            )
                        )

        elif device.os == "ios" or device.os == "iosxe":
            for ntp_server_ip in ntp_server_ip_list:
                try:
                    # store command result for later usage
                    result = device.ping(ntp_server_ip)

                except Exception as e:

                    match = re.search(r"(?P<success_rate_is>\d+) percent", str(e))
                    success_rate = match.group("success_rate_is")
                    self.failed(
                        "FAILED: Ping NTP Server {} from device {} with success rate of {}%\n".format(
                            ntp_server_ip, device.name, success_rate
                        )
                    )
                    log.info(
                        "FAILED: Ping NTP Server {} from device {} with success rate of {}%".format(
                            ntp_server_ip, device.name, success_rate
                        )
                    )
                else:
                    # extract success rate from ping result with regular expression
                    match = re.search(r"(?P<success_rate_is>\d+) percent", result)
                    success_rate = match.group("success_rate_is")
                    if float(success_rate) > 0:
                        # ping responded
                        self.passed(
                            "PASSED: Ping NTP Server {} from device {} with with success rate of {}%".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )
                        log.info(
                            "PASSED: Ping NTP Server {} from device {} with with success rate of {}%".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )
                    else:
                        # packet loss was 100%
                        self.failed(
                            "FAILED: Ping NTP Server {} from device {} with with success rate of of {}%".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )
                        log.info(
                            "FAILED: Ping NTP Server {} from device {} with with success rate of of {}%".format(
                                ntp_server_ip, device.name, success_rate
                            )
                        )

        else:
            self.failed(
                "FAILED: Device OS type {} not handled in script for device {}\n".format(
                    device.os, device
                )
            )
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
        pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
