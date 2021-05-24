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
import re
from pyats.topology import loader

# Get your logger for your script
global log
log = logging.getLogger(__name__)
log.level = logging.INFO


#test result recording
test_status_string = ''
test_status = 'None'
pass_counter = 0


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
        global test_status_string 
        global test_status
        global pass_counter
        genie_testbed = Genie.init(testbed)
        self.parent.parameters['testbed'] = genie_testbed
        device_list = []
        for device in genie_testbed.devices.values():
            
            try:
                device.connect(log_stdout=False)
                device_list.append(device)
                test_status_string = test_status_string + (f"PASSED: Establish "f"connection to '{device.name}'\n")
                pass_counter += 1
                
            except errors.ConnectionError:
                #self.skipped(f"Failed to establish "f"connection to '{device.name}'")
                test_status_string = test_status_string + (f"FAILED: Unable to establish "f"connection to '{device.name}'\n")
                test_status = 'Failed'
                

        # Pass list of devices to testcases
        self.parent.parameters.update(dev=device_list)


class Check_LLDP(aetest.Testcase):
    """
    Version Testcase - extract LLDP config from devices
    """

    @aetest.setup
    def setup(self):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """

        devices = self.parent.parameters['dev']
        log.info(devices)
        aetest.loop.mark(self.check_lldp, device=devices)

    @aetest.test
    def check_lldp(self, device):
        """
       
        """
        global test_status_string
        global test_status
        global pass_counter

        if device.os == 'WIP':
            pass

        elif device.os == 'nxos':
            lldp_details = device.execute('show running-config | include feature lldp')
            if lldp_details == '': 
                test_status_string = test_status_string + 'FAILED: LLDP is not configured on {} \n'.format(device)
                test_status = 'Failed'
                log.info('FAILED: LLDP is not configured on {}'.format(device))

            elif lldp_details.find('feature lldp') != -1:
                #check for lldp written in the returned wording
                test_status_string = test_status_string + 'PASSED: LLDP on {} set\n'.format(device)
                pass_counter += 1
                log.info('PASSED: LLDP is configured on {}'.format(device))

        elif device.os == 'ios':
            lldp_details = device.execute('show running-config | include lldp run')
            if lldp_details == '': 
                test_status_string = test_status_string + 'FAILED: LLDP is not configured on {}\n'.format(device)
                test_status = 'Failed'
                log.info('FAILED: LLDP is not configured on {}'.format(device))

            elif lldp_details.find('lldp run') != -1:
                #check for lldp written in the returned wording
                test_status_string = test_status_string + 'PASSED: LLDP is configured on {}\n'.format(device)
                pass_counter += 1
                log.info('PASSED: LLDP is configured on {}'.format(device))

        else:
            test_status_string = test_status_string + 'FAILED: Device OS type {} not handled in script for device {}\n'.format(device.os,device)
            test_status = 'Failed'
            log.info('FAILED: Device OS type {} not handled in script for device {}'.format(device.os,device))
     
            
class CommonCleanup(aetest.CommonCleanup):
    """CommonCleanup Section
    < common cleanup docstring >
    """

    # uncomment to add new subsections
    @aetest.subsection
    def subsection_cleanup_one(self):
        global test_status_string
        global test_status
        global pass_counter
        if test_status == 'Failed':
            self.failed(f"FAILED: Check LLDP Test\n{test_status_string}")
        if test_status =='None' and pass_counter == 0:
            self.failed(f"FAILED: Check LLDP anomaly, check script\n{test_status_string}")
        if test_status =='None' and pass_counter > 0:
            self.passed(f'PASSED: Check LLDP\n{test_status_string}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--testbed', dest='testbed',
                        type=loader.load)

    args, unknown = parser.parse_known_args()

    aetest.main(**vars(args))