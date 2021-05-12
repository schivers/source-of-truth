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

# interfaces:
interface_types_to_check_list = ['Ethernet','mgmt']

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
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            log.info(banner(f"Connect to device '{device.name}'"))
            try:
                device.connect(log_stdout=False)
            except errors.ConnectionError:
                self.failed(f"Failed to establish "
                            f"connection to '{device.name}'")
            device_list.append(device)
        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class CDP(aetest.Testcase):
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

        devices = self.parent.parameters['dev']
        aetest.loop.mark(self.cdp_enabled, device=devices)

    @aetest.test
    def cdp_enabled(self, device):
        """
        Verify that the OS version is correct
        """
        test_status = 'None'
        pass_counter = 0
        test_status_string = ''

        if device.os == 'iosxe':

            pass

        elif device.os == 'ios':

            pass

        elif device.os == 'nxos':

            out = device.parse('show interface')
            for interface in out.items():
                for interfaces_types_to_check in interface_types_to_check_list:
                    if interface[0].find(interfaces_types_to_check) != -1:
                        interface_detail = device.execute('show cdp interface ' + interface[0])
                        interface_detail_line_array = interface_detail.splitlines()
                        line_index = 0
                        cdp_enabled = False
                        while line_index < len(interface_detail_line_array):
                            if interface_detail_line_array[line_index].find('CDP enabled') != -1:
                                cdp_enabled = True
                            line_index += 1
                        if cdp_enabled:
                            log.info(f"{interface[0]} on {device} PASSED: cdp enabled")
                            pass_counter += 1
                        else:
                            log.info(f"{interface[0]} on {device} FAILED: cdp disabled")
                            test_status = 'Failed'
                            test_status_string = f'{test_status_string} {interface[0]} on {device} FAILED: cdp disabled\n'

            if test_status == 'Failed':
                self.failed(f"{device} FAILED: cdp disabled\n{test_status_string}")
            if test_status =='None' and pass_counter == 0:
                self.failed(f"{device} FAILED: no interfaces passed or failed, check script")
            if test_status =='None' and pass_counter > 0:
                self.passed(f'{device} all interfaces checked are enabled for cdp')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed',
                        type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))