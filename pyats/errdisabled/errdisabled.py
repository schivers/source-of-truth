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
            testbed.connect(
                learn_hostname=True,
                log_stdout=False,
                connection_timeout=60,
                init_config_commands=[],
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
            aetest.loop.mark(err_disabled, device=device_list, uids=d_name)

        else:
            self.failed()


class err_disabled(aetest.Testcase):
    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """
        pass

    @aetest.test
    def test(self, device):
        "Check errdisabled recovery feature set up correctly"
        if device.os == "iosxe" or device.os == "ios":
            errDisabledCase = [
                "errdisable recovery cause udld",
                "errdisable recovery cause bpduguard",
                "errdisable recovery cause mac-limit",
                "errdisable recovery cause storm-control",
                "errdisable recovery interval 900",
            ]
            log.info("Expected config:{0}".format(errDisabledCase))
            out1 = device.api.get_running_config("errdisable")
            log.info("ErrDisabled:{0}".format(out1))
            # List comprehension checking all elements of a list are present
            result = all(elem in out1 for elem in errDisabledCase)

            if result:
                self.passed("ErrDisabled Recovery configuration is valid.")
            else:
                self.failed("ErrDisabled Recovery configuration is invalid.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
