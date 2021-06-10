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
                    log.warning(f"{device_name} connected status: {device.connected}")
                    step.skipped()

        # Pass list of devices to testcases
        if device_list:
            # ADD NEW TESTS CASES HERE
            aetest.loop.mark(eigrp, device=device_list, uids=d_name)

        else:
            self.failed()


class eigrp(aetest.Testcase):
    """
    Validate the Core router's downlink connection torwards the Core switches.
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

    @aetest.test
    def global_eigrp(self, device):
        "Check Global routing EIGRP neighbours table has 3 EIGRP Neighbours"

        if device.os == "iosxe":
            out1 = device.parse("show ip eigrp neigh")
            log.info(out1)
            uptime_eigrp = out1.q.contains("eigrp_interface").get_values("uptime")
            if len(uptime_eigrp) == 3:
                self.passed("Three EIGRP neighbours found")
            else:
                self.failed("{0} EIGRP neighbours found".format(len(uptime_eigrp)))

        else:
            self.skipped("Test skipped - Device not compatible.")

    @aetest.test
    def eigrp_vrf(self, device, steps):
        "Check EIGRP neighbours table in each VRF has 3 EIGRP Neighbours"
        vrf_list = [
            "AFP",
            "AP",
            "BROADCASTER",
            "COMPETITION",
            "EPA",
            "GETTY",
            "HOSPITALITY",
            "MEDIA",
            "PCI",
            "REUTERS",
            "SUPPLIER",
            "VOIP",
        ]
        if device.os == "iosxe":
            for i in vrf_list:
                with steps.start(f"Test EIGRP VRF {i}", continue_=True) as step:
                    command = "show ip eigrp vrf {0} neighbors".format(i)
                    out1 = device.parse(command)
                    uptime_eigrp = out1.q.contains("eigrp_interface").get_values(
                        "uptime"
                    )
                    if len(uptime_eigrp) == 3:
                        step.passed("Three EIGRP neighbours found")
                    else:
                        step.failed(
                            "{0} EIGRP neighbours found".format(len(uptime_eigrp))
                        )

        else:
            self.skipped("Test failed - Device not compatible.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--testbed", dest="testbed", type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))
