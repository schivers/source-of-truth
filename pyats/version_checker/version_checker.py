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
from pyats.topology import loader

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO

# Software versions:
iosxe_os = ["16.12.5"]
ios_os = ["15.2(7)E3"]
nxos_os = ["9.3(9)"]


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

        genie_testbed = Genie.init(testbed)
        self.parent.parameters["testbed"] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(f"Connect to device '{device.name}'"))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(f"Failed to establish " f"connection to '{device.name}'")
            device_list.append(device)
        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class Version(aetest.Testcase):
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

        devices = self.parent.parameters["dev"]
        aetest.loop.mark(self.version, device=devices)

    @aetest.test
    def version(self, device):
        """
        Verify that the OS version is correct
        """

        if device.os == "iosxe":

            out1 = device.parse("show version")
            os_version = out1["version"]["version"]

            if os_version not in iosxe_os:
                self.failed(f"{os_version} on {device} is not the correct version")
            else:
                pass

        elif device.os == "ios":

            out2 = device.parse("show version")
            os_version = out2["version"]["version"]

            if os_version not in ios_os:
                self.failed(f"{os_version} on {device} is not the correct version")
            else:
                pass

        elif device.os == "nxos":

            out3 = device.parse("show version")
            pprint.pprint(out3)
            os_version = out3["platform"]["software"]["system_version"]

            if os_version not in nxos_os:
                self.failed(f"{os_version} on {device} is not the correct version")
            else:
                pass


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
