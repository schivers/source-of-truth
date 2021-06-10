"""
interface_errors.py
Verify that no errors have been reported on network interfaces in the testbed.
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

__author__ = "Hank Preston"
__copyright__ = "Copyright (c) 2019, Cisco Systems Inc."
__contact__ = ["hapresto@cisco.com"]
__credits__ = []
__version__ = 1.0

import logging

from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)


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
            logger.error("NOT CONNECTED TO ALL DEVICES")

    @aetest.subsection
    def verify_connected(self, testbed, steps):
        device_list = []
        d_name = []
        for device_name, device in testbed.devices.items():

            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                logger.info(device)
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                    device_list.append(device)
                    d_name.append(device_name)
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.skipped()

        # Pass list of devices to testcases
        if device_list:
            # ADD NEW TESTS CASES HERE
            # aetest.loop.mark(interface_errors, device=device_list,uids=d_name)
            pass

        else:
            self.failed()


class interface_errors(aetest.Testcase):
    """interface_errors
    < docstring description of this testcase >
    """

    # List of counters keys to check for errors
    #   Model details: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    counter_error_keys = ("in_crc_errors", "in_errors", "out_errors")

    @aetest.setup
    def setup(self, testbed):
        """Learn and save the interface details from the testbed devices."""
        self.learnt_interfaces = {}
        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            logger.info(f"{device_name} connected status: {device.connected}")
            if device.os in ("ios", "iosxe", "iosxr", "nxos") and device.connected:
                logger.info(f"Learning Interfaces for {device_name}")
                self.learnt_interfaces[device_name] = device.learn("interface").info

    @aetest.test
    def test(self, steps):
        # Loop over every device with learnt interfaces
        for device_name, interfaces in self.learnt_interfaces.items():
            with steps.start(
                f"Looking for Interface Errors on {device_name}", continue_=True
            ) as device_step:

                # Loop over every interface that was learnt
                for interface_name, interface in interfaces.items():
                    with device_step.start(
                        f"Checking Interface {interface_name}", continue_=True
                    ) as interface_step:

                        # Verify that this interface has "counters" (Loopbacks Lack Counters on some platforms)
                        if "counters" in interface.keys():
                            # Demonstration: Updating a test to log more details
                            #   Uncomment the below logger.info line to write to the log the contents of the "counters" key
                            logger.info(
                                f"Device {device_name} Interface {interface_name} counters: {interface['counters']}"
                            )

                            # Loop over every counter to check, looking for values greater than 0
                            for counter in self.counter_error_keys:
                                # Verify that the counter is available for this device
                                if counter in interface["counters"].keys():
                                    if interface["counters"][counter] > 0:
                                        interface_step.failed(
                                            f'Device {device_name} Interface {interface_name} has a count of {interface["counters"][counter]} for {counter}'
                                        )
                                else:
                                    # if the counter not supported, log that it wasn't checked
                                    logger.info(
                                        f"Device {device_name} Interface {interface_name} missing {counter}"
                                    )
                        else:
                            # If the interface has no counters, mark as skipped
                            interface_step.skipped(
                                f"Device {device_name} Interface {interface_name} missing counters"
                            )


if __name__ == "__main__":
    # for stand-alone execution
    import argparse
    from pyats import topology

    # from genie.conf import Genie

    parser = argparse.ArgumentParser(description="standalone parser")
    parser.add_argument(
        "--testbed",
        dest="testbed",
        help="testbed YAML file",
        type=topology.loader.load,
        # type=Genie.init,
        default=None,
    )

    # do the parsing
    args = parser.parse_known_args()[0]

    aetest.main(testbed=args.testbed)
