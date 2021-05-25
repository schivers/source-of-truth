"""
Baku_test_job.py
"""
# see https://pubhub.devnetcloud.com/media/pyats/docs/easypy/jobfile.html
# for how job files work

__author__ = "Shaun Chivers"
__copyright__ = "NTT Global"
__contact__ = ["shaun.chivers@global.ntt"]
__credits__ = ["Hank Preston, Cisco Systems"]
__version__ = 1.0

import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""

    # run script
    run(
        testscript=os.path.join(SCRIPT_PATH, "testbed_connectivity.py"),
        runtime=runtime,
        taskid="Validate Connectivity",
    )
    #    run(
    #        testscript=os.path.join(SCRIPT_PATH, "hostname_checker.py"),
    #        runtime=runtime,
    #        taskid="Check Configured Hostname",
    #     )

    run(
        testscript=os.path.join(SCRIPT_PATH, "interface_errors.py"),
        runtime=runtime,
        taskid="Interface Errors",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "version_checker.py"),
        runtime=runtime,
        taskid="Version Checker",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "ping_central_ntp.py"),
        runtime=runtime,
        taskid="Ping Central NTP Server",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "ping_configured_ntp.py"),
        runtime=runtime,
        taskid="Ping Configured NTP Servers",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "check_snmp_settings.py"),
        runtime=runtime,
        taskid="Check SNMP Settings",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "check_ntp_associations.py"),
        runtime=runtime,
        taskid="Check NTP Associations",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "check_lldp.py"),
        runtime=runtime,
        taskid="Check LLDP Settings",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "check_dns_server_settings.py"),
        runtime=runtime,
        taskid="Check DNS Server Settings",
    )

    run(
        testscript=os.path.join(SCRIPT_PATH, "cdp_enabled.py"),
        runtime=runtime,
        taskid="Check CDP Enabled Per Interface",
    )
