#!/usr/bin/env python3

# To get a logger for the script
import logging
from pyats import aetest
from pyats.log.utils import banner

# Genie Imports
from genie.conf import Genie

# To handle errors with connections to devices
from unicon.core import errors
import argparse
from pyats.topology import loader

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO


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
            log.info(device)
            log.info(banner(f"Connect to device '{device.name}'"))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(f"Failed to establish " f"connection to '{device.name}'")
                continue
            device_list.append(device)
        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class check_syslog(aetest.Testcase):
    """
    Check Syslog settings
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

        devices = self.parent.parameters["dev"]
        aetest.loop.mark(self.test, device=devices)

    @aetest.test
    def test(self, device):
        syslog = "172.22.192.56"
        "Check VTP Status for domain name & operation mode."
        if device.os == "iosxe" or device.os == "ios":
            out1 = device.api.get_running_config("logging host {0}".format(syslog))
            if out1:
                self.passed("Syslog setting found for {0}".format(syslog))
            else:
                self.failed("Syslog setting not found.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
