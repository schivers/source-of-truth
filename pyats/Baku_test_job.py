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
    """
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
    """
    run(
       testscript=os.path.join(SCRIPT_PATH, "cdp_enabled2.py"),
       runtime=runtime,
       taskid="CDP Enabled",
    )