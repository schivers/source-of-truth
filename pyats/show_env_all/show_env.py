"""
show_processes_cpu.py
Verify the CPU Utlisation is not exceeding 75 percent for more than 5 minutes
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/aetest/index.html
# for documentation on pyATS test scripts

import logging
from pyats import aetest
from genie.testbed import load
import logging
from genie import parsergen
import re
from genie.utils import Dq
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

global log
log = logging.getLogger(__name__)
log.level = logging.INFO

class CommonSetup(aetest.CommonSetup):
    @aetest.subsection
    def connect(self, testbed):
        """
        establishes connection to all your testbed devices.
        """
        # make sure testbed is provided
        assert testbed, "Testbed is not provided!"

        # connect to all testbed devices
        #   By default ANY error in the CommonSetup will fail the entire test run
        #   Here we catch common exceptions if a device is unavailable to allow test to continue
        try:
           testbed.connect(
                learn_hostname=True, log_stdout=False, connection_timeout=60
            )
        except (TimeoutError, StateMachineError, ConnectionError):
            log.error("Unable to connect to all devices")

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
            aetest.loop.mark(Environment_Checks, device=device_list, uids=d_name)

        else:
            self.failed()
    
    


class Environment_Checks(aetest.Testcase):
    """
    Check the CPU Utilisation of all the devices in the testbed.yaml
    Report a failure if a CPU Process exceeds 75 Percent for more
    than 5 minutes
    """

    # List of counters keys to check for errors
    #   Model details: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    @aetest.setup
    def setup(self,device):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """
        self.execute_env = []
        
        if device.os == "ios":
            try:
                out = device.execute("show env all")

            except Exception as e:
                self.failed("Exception occured ".format(str(e)))
            #print(out)
            out= out.splitlines()
            #print(out1)
            self.execute_env=out
        if device.os == "iosxe":
            out = device.execute("show environment")
            print(out)
            self.execute_env= out
            print(self.execute_env)

    @aetest.test
    def Check_Temp(self,device):
        if device.os == "ios":
            out1= [i for i in self.execute_env if "SYSTEM TEMPERATURE is" in i ]
            print(self.execute_env)
            if not "SYSTEM TEMPERATURE is OK" in self.execute_env: 
                self.failed("System Temperature not healthy:{0}".format(out1))
            else: 
                self.passed("System Temperature is healthy")
        if device.os == "iosxe":
             self.skipped("XE device not compatible with test.")
        
    @aetest.test
    def Check_Temp_State(self,device):
        if device.os == "ios":
            out1= [i for i in self.execute_env if "System Temperature State" in i ]
            print(self.execute_env)
            if not "System Temperature State: GREEN" in self.execute_env: 
                self.failed("System Temperature State not healthy:{0}".format(out1))
            else: 
                self.passed("System Temperature State is healthy")
        if device.os == "iosxe":
             self.skipped("XE device not compatible with test.")

    @aetest.test
    def Check_Power_State(self,device):
        if device.os == "ios":
            out1= [i for i in self.execute_env if "Power Supply Status:" in i ]
            print(self.execute_env)
            if not "Power Supply Status: Good" in self.execute_env: 
                self.failed("System Power Supply Status is not healthy:{0}".format(out1))
            else: 
                self.passed("System Power Supply Status is healthy")
        if device.os == "iosxe":
             self.skipped("XE device not compatible with test.")
    
    @aetest.test
    def Check_Fan_State(self,device):
        if device.os == "ios":
            out1= [i for i in self.execute_env if "SYSTEM FAN SPEED is" in i ]
            print(self.execute_env)
            if not "SYSTEM FAN SPEED is" in self.execute_env: 
                self.skipped("Device has no Fan information")
            elif not "SYSTEM FAN SPEED is OK": 
                self.failed("System Fan Speed is not healthy:{0}".format(out1))
            else:
                self.passed("System Fan Speed is healthy")
        if device.os == "iosxe":
             self.skipped("XE device not compatible with test.")
    
    # @aetest.test
    # def Check_XE_State(self,device):
    #     if device.os == "ios":
    #         self.skipped("IOS device not compatible with test.")
    #     if device.os == "iosxe":
    #         header=['Slot','Sensor','Current State','Reading','Threshold\(Minor,Major,Critical,Shutdown\)']
    #         out1= self.execute_env
    #         out1 = re.sub('%',' ', out1)
    #         print(out1)
    #         result = parsergen.oper_fill_tabular(device_output=out1, device_os='iosxe',header_fields=header, index=[1])
    #         print(result)
    #         output=result.entries
    #         print(output)
    #         XE_State= Dq(output).contains('Current State').not_contains('Normal').reconstruct()
    #         print(XE_State)


    
            
                
                

    

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
