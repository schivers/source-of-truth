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
from pyats.async_ import pcall

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
            aetest.loop.mark(Version, device=device_list, uids=d_name)

        else:
            self.failed()


# Software versions:
iosxe_os = ["16.12.5", "16.09.06", "16.12.4"]
ios_os = ["15.2(7)E3"]
nxos_os = ["9.3(9)"]


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

        #devices = self.parent.parameters["dev"]
        #aetest.loop.mark(self.version, device=devices)

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
                self.passed(f"{os_version} on {device} is the correct version")

        elif device.os == "ios":

            out2 = device.parse("show version")
            os_version = out2["version"]["version"]

            if os_version not in ios_os:
                self.failed(f"{os_version} on {device} is not the correct version")
            else:
                self.passed(f"{os_version} on {device} is the correct version")

        elif device.os == "nxos":

            out3 = device.parse("show version")
            
            os_version = out3["platform"]["software"]["system_version"]

            if os_version not in nxos_os:
                self.failed(f"{os_version} on {device} is not the correct version")
            else:
                self.passed(f"{os_version} on {device} is the correct version")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
