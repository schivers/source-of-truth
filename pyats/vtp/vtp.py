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
            testbed.connect(log_stdout=False)
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
            aetest.loop.mark(vtp_status, device=device_list, uids=d_name)

        else:
            self.failed()


class vtp_status(aetest.Testcase):
    """
    Check VTP Status for domain name & operation mode.
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

        # devices = self.parent.parameters["dev"]
        # aetest.loop.mark(self.test, device=devices)

    @aetest.test
    def test(self, device, steps):
        "Check VTP Status for domain name & operation mode."
        with steps.start("Executing 'show vtp status' on {0}".format(device.name)):

            if device.os == "iosxe" or device.os == "ios":
                out1 = device.parse("show vtp status")
                log.info(out1)

            else:
                self.failed("Test failed - Device not compatible.")

        with steps.start(
            "Validating VTP Domain Name for {0}".format(device.name), continue_=True
        ) as step:

            if out1:
                domain_name = out1["vtp"]["domain_name"]
                if domain_name == device.hostname:
                    step.passed("Domain Name matches with Hostname")
                else:
                    step.failed(
                        "Domain Name ({0}) does not match with Hostname ({1})".format(
                            domain_name, device.hostname
                        )
                    )

        with steps.start(
            "Validating VTP Operation Mode {0}".format(device.name)
        ) as step:

            if out1:
                operating_mode = out1["vtp"]["operating_mode"]
                if operating_mode == "transparent":
                    step.passed("Operating mode is set to '{0}'".format(operating_mode))
                else:
                    step.failed("Operating mode is set to '{0}'".format(operating_mode))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
