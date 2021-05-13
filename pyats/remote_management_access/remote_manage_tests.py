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
            device_list.append(device)
        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class RemoteManagement(aetest.Testcase):
    """
    Verify the following:
    - Hostname
    - Configured credentials
    - Domain Name Configuration
    - Crypto Key Existence
    - SSH Version
    - 'transport input ssh' under line vty 0
    - AAA settings
    - Enable Secret
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

        devices = self.parent.parameters["dev"]
        aetest.loop.mark(self.host_checker, device=devices)
        aetest.loop.mark(self.show_users, device=devices)
        aetest.loop.mark(self.show_domain_name, device=devices)
        aetest.loop.mark(self.show_crypto_key, device=devices)
        aetest.loop.mark(self.ssh_version, device=devices)
        aetest.loop.mark(self.line_vty, device=devices)
        aetest.loop.mark(self.show_enable_secret, device=devices)
        aetest.loop.mark(self.show_aaa_settings, device=devices)
        aetest.loop.mark(self.show_enable_secret, device=devices)

    @aetest.test
    def host_checker(self, device):
        "Alternative method of checking hostname - dev.connect() automatically finds the current hostname unless specified dev.connect(learn_hostname=False)"
        if device.hostname != device.name:
            self.failed(
                "{0} does not match with inventory hostname - {1}".format(
                    device.hostname, device.name
                )
            )
        else:
            pass

    @aetest.test
    def show_users(self, device):
        "Show Users"
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("show run | include username")
            log.info("Configured Users: \n {0}".format(out1))

        elif device.os == "nxos":
            out1 = device.execute("show run | include username")
            log.info("Configured Users:\n {0}".format(out1))

    @aetest.test
    def show_domain_name(self, device):
        "Check domain-name configuration"
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("show run | include ip domain name")
            log.info("Domain name: {0}".format(out1))

        elif device.os == "nxos":
            out1 = device.execute("show run | include domain-name")
            log.info("Domain name: {0}".format(out1))

    @aetest.test
    def show_crypto_key(self, device):
        "Return the output from keys found on an IOS/XE device"
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("show crypto key mypubkey rsa | include Key name")
            log.info("Keys Found:\n {0}".format(out1))

        elif device.os == "nxos":
            pass

    @aetest.test
    def ssh_version(self, device):
        "Returns a single line of text to indicate if SSH is enabled."
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("sh ip ssh | include SSH")
            log.info(out1)
            if "Enabled" in out1:
                self.passed("SSH is enabled on this device.")
            else:
                self.failed("SSH is not enabled - {0}".format(out1))

        elif device.os == "nxos":
            out1 = device.execute("sh ssh server")
            log.info(out1)

    @aetest.test
    def line_vty(self, device):
        "Validate 'transport input ssh' under line vty 0 X. Nexus does not have this option"
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("sh run | sec line vty 0")
            log.info(out1)
            if "transport input ssh" in out1:
                self.passed("transport input ssh found under line vty 0")
            else:
                self.failed("'transport input ssh' line was not found")

        elif device.os == "nxos":
            pass

    @aetest.test
    def show_aaa_settings(self, device):
        "Verify AAA Settings"
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("show run | section aaa")
            log.info("AAA Settings:\n {0}".format(out1))

        elif device.os == "nxos":
            out1 = device.execute("show run | section aaa")
            log.info("Domain name:\n {0}".format(out1))

    @aetest.test
    def show_enable_secret(self, device):
        "Verify Enable Secret"
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("show run | include enable secret")
            log.info("Enable Secret: {0}".format(out1))

        elif device.os == "nxos":
            out1 = device.execute("show run | include enable secret")
            log.info("Enable Secret: {0}".format(out1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
