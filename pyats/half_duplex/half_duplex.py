"""
half_duplex.py
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

import logging

from pyats import aetest
from genie.testbed import load
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

# create a logger for this module
logger = logging.getLogger(__name__)

###################################################################
#                  COMMON SETUP SECTION                           #
###################################################################


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
            logger.error("NOT CONNECTED TO ALL DEVICES")

    @aetest.subsection
    def verify_connected(self, testbed, steps):
        for device_name, device in testbed.devices.items():
            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                logger.info(device)
                if device.connected:
                    logger.info(f"{device_name} connected status: {device.connected}")
                else:
                    logger.error(f"{device_name} connected status: {device.connected}")
                    step.skipped()


###################################################################
#                     TESTCASES SECTION                           #
###################################################################


class interface_duplex(aetest.Testcase):
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
                f"Looking for half-duplex Interfaces on {device_name}", continue_=True
            ) as device_step:

                # Loop over every interface that was learnt
                for interface_name, interface in interfaces.items():
                    with device_step.start(
                        f"Checking Interface {interface_name}", continue_=True
                    ) as interface_step:

                        # Verify that this interface has "duplex_mode" (Virtual interfaces Lack duplex)
                        if "duplex_mode" in interface.keys():
                            if interface["duplex_mode"] == "half":
                                interface_step.failed(
                                    f"Device {device_name} Interface {interface_name} is in half-duplex mode"
                                )
                        else:
                            # If the interface has no duplex, mark as skipped
                            interface_step.skipped(
                                f"Device {device_name} Interface {interface_name} has no duplex"
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
