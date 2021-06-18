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
                learn_hostname=True,
                log_stdout=False,
                connection_timeout=60,
                init_config_commands=[],
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
            aetest.loop.mark(Power_Check, device=device_list, uids=d_name)

        else:
            self.failed()


class Power_Check(aetest.Testcase):
    """
    Check the CPU Utilisation of all the devices in the testbed.yaml
    Report a failure if a CPU Process exceeds 75 Percent for more
    than 5 minutes
    """

    # List of counters keys to check for errors
    #   Model details: https://pubhub.devnetcloud.com/media/genie-feature-browser/docs/_models/interface.pdf
    @aetest.setup
    def setup(self, device):
        """
        Get list of all devices in testbed and
        run version testcase for each device
        """
        self.parse_power = {}

        if device.os in ("ios"):
            try:
                out = device.parse("show power inline")

            except Exception as e:
                self.failed("Exception occured {0} ".format(str(e)))
            print(out)
            self.execute_env = out

    @aetest.test
    def Check_Power(self, device):
        if device.os in ("ios"):
            out1 = self.execute_env
            output = Dq(out1).contains("^[0-9]+$", regex=True).get_values("remaining")
            print(output)
            for i in output:
                if i <= 24:
                    self.failed("Power remaining is less than 24W: {0}".format(output))
                else:
                    next
            self.passed("Power remaining is sufficient.")


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
