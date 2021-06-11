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
        for device_name, device in testbed.devices.items():
            with steps.start(
                f"Test Connection Status of {device_name}", continue_=True
            ) as step:
                # Test "connected" status
                log.info(device)
                if device.connected:
                    log.info(f"{device_name} connected status: {device.connected}")
                else:
                    log.error(f"{device_name} connected status: {device.connected}")
                    step.skipped()

    def set_store_num(self, store):
        aetest.loop.mark
    
    


class CPU_utilisation_checks(aetest.Testcase):
    """
    Check the CPU Utilisation of all the devices in the testbed.yaml
    Report a failure if a CPU Process exceeds 75 Percent for more
    than 5 minutes
    """

    # List of counters keys to check for errors
    #   Model details: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    @aetest.setup
    def setup(self, testbed):
        """Check the Network OS matches the Testbed.yaml file"""
        self.execute_cpu = {}
        self.execute_cpu_history={}
        self.output = {}
        #MODIFY
        #CPU Max 
        self.cpu_max=90
        self.cpu_max_pids=60
        self.cpu_avg= 80

        for device_name, device in testbed.devices.items():
            # Only attempt to learn details on supported network operation systems
            if device.os in ("iosxe","iosxr","ios","nxos") and device.connected:
                log.info(f"{device_name} connected status: {device.connected}")
                log.info(f"Running the show processes cpu command for {device_name}")
                self.execute_cpu[device_name] = device.parse("show processes cpu")
                self.execute_cpu_history[device_name] = device.parse("show processes cpu history")

    @aetest.test
    def Check_CPU(self, steps):
        for device_name, device in self.execute_cpu.items():
            with steps.start(
                f"Checking  5min CPU(%) {device_name}", continue_=True
            ) as device_step:
                output = self.execute_cpu[device_name]
                output = output["five_min_cpu"]
                if output>=self.cpu_max:
                    device_step.failed(
                        f"Very High 5 Minute CPU detected on {device_name}"
                    )

                else:
                    device_step.passed(
                        f"No issues found with the CPU Utilisation on {device_name}"
                    )
                

    @aetest.test
    def Check_CPU_PIDS(self, steps):
        for device_name, device in self.execute_cpu.items():
            with steps.start(
                f"Checking CPU(%) PIDs for {device_name}", continue_=True
            ) as device_step:

                print(device_name)
                output = self.execute_cpu[device_name]
                output = output["sort"]
                cpu_bad = (
                    Dq(output).value_operator("five_min_cpu", ">=", 5).reconstruct()
                )
                #print(output)
                process_id = str(cpu_bad.keys())
                if cpu_bad != {}:
                    device_step.failed(
                        f"Very High 5 Minute CPU detected on {device_name} with the following Process ID {process_id}"
                    )

                else:
                    device_step.passed(
                        f"No issues found with the CPU Utilisation on {device_name}"
                    )

    @aetest.test
    def Check_History(self, steps):
        for device_name, device in self.execute_cpu_history.items():
        
            output = self.execute_cpu_history[device_name]
            print(output)
            output = output["72h"]

            cpu_max_bad = (
                Dq(output).value_operator("maximum", ">=", self.cpu_max).reconstruct()
            )
            cpu_avg_bad = (
                Dq(output).value_operator("average", ">=", self.cpu_avg).reconstruct()
            )
            max_cpu_hours = str(list(cpu_max_bad.keys()))
            avg_cpu_hours = str(list(cpu_avg_bad.keys()))
            with steps.start(
            f"Checking Max CPU(%) 72 HR History {device_name}", continue_=True
        ) as max_step:
                if cpu_max_bad != {}:
                    max_step.failed(
                        f"Very High MAX CPU detected on {device_name} in the last {max_cpu_hours} hours "
                    )
                else:
                    max_step.passed(
                        f"No issues found with the CPU Utilisation on {device_name}"
                    )
            with steps.start(
            f"Checking Avg CPU(%) 72 HR History {device_name}", continue_=True
        ) as avg_step:
                if cpu_avg_bad != {}:
                    avg_step.failed(
                    f"Very High AVG CPU detected on {device_name} in the last {avg_cpu_hours} hours"
                )
                    
                else:
                    avg_step.passed(
                        f"No issues found with the average CPU Utilisation on {device_name} in last 72 Hours."
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
