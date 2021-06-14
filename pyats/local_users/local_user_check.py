#!/bin/env python
import logging
from pyats import aetest
from pyats.log.utils import banner
from genie.conf import Genie
from genie.libs import ops  # noqa
from unicon.core.errors import TimeoutError, StateMachineError, ConnectionError

log = logging.getLogger(__name__)


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
            aetest.loop.mark(local_user_check, device=device_list,uids=d_name)
            

        else:
            self.failed()


class local_user_check(aetest.Testcase):

    groups = ["aaa", "golden_config"]

    @aetest.test
    def compare_local_users(self, steps, device, expected_local_users):
        """Local User Database checks

        Given a list of expected usernames validates they
        are present on the device

        """
        #device = self.parent.parameters["testbed"].devices[dev_name]
        with steps.start("Getting Configured Usernames"):
            usernames = device.execute("show run | inc username")
            lines = usernames.split("\r\n")
            cfg_local_users = [w.split(" ")[1] for w in lines]
            log.info("Configured Users: {}".format(cfg_local_users))

        with steps.start("Comparing Configured Usernames"):
            msg = "Checking for {} in local user database"
            log.info(msg.format(expected_local_users))
            if not sorted(expected_local_users) == sorted(cfg_local_users):
                self.failed("User lists are not same")


if __name__ == "__main__":  # pragma: no cover
    aetest.main()
