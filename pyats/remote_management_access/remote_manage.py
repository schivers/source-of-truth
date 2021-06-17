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


class CommonSetup(aetest.CommonSetup):
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

        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        try:
            testbed.connect(log_stdout=False, learn_hostname=True)
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
            aetest.loop.mark(RemoteManagement, device=device_list, uids=d_name)

        else:
            self.failed()


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
            users = ["username admin", "username solarwinds"]
            out1 = device.api.get_running_config("username")

            log.info("Configured Users: \n {0}".format(out1))
            # List comprehension
            res = [elem for elem in out1 if any(i in elem for i in users)]

            log.info("Filtered Users:{0}".format(res))

            if len(res) == len(users):
                self.passed("Configured users were found.")
            else:
                self.failed("Configured users not found.")

        elif device.os == "nxos":
            out1 = device.execute("show run | include username")
            log.info("Configured Users:\n {0}".format(out1))

    @aetest.test
    def show_domain_name(self, device):
        "Check domain-name configuration"
        if device.os == "iosxe" or device.os == "ios":
            domainTestCase = [
                "ip domain-name uefa.local",
                "ip name-server 10.224.0.100",
            ]

            out1 = device.api.get_running_config_section("ip")
            log.info("Domain name: {0}".format(out1))
            result = all(elem in out1 for elem in domainTestCase)

            if result:
                self.passed("Domain Name configuration is correct.")
            else:
                self.failed("Domain Name configuration does not match")

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
        "Verify AAA Settings -show run | section aaa"
        if device.os == "iosxe" or device.os == "ios":
            aaaTestCase = [
                "aaa new-model",
                "aaa authentication login default local",
                "aaa authorization exec default local if-authenticated ",
            ]
            log.info("Expected config:\n{0}".format(aaaTestCase))
            out1 = device.api.get_running_config_section("aaa")
            log.info("AAA Settings:\n {0}".format(out1))
            result = all(elem in out1 for elem in aaaTestCase)

            if result:
                self.passed("AAA Settings are correct")
            else:
                self.failed("AAA settings do not match with test case")

        elif device.os == "nxos":
            out1 = device.execute("show run | section aaa")
            log.info("Domain name:\n {0}".format(out1))

    @aetest.test
    def show_enable_secret(self, device):
        "Verify Enable Secret"
        if device.os == "iosxe" or device.os == "ios":

            out1 = device.execute("show run | include enable secret")
            if out1:
                self.passed("Enable Secret - {0}".format(out1))
            else:
                self.failed("Enable Secret was not found.")

        elif device.os == "nxos":
            out1 = device.execute("show run | include enable secret")
            log.info("Enable Secret: {0}".format(out1))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
