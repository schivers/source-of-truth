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

    run(
        testscript=os.path.join(SCRIPT_PATH, "show_power.py"),
        runtime=runtime,
        taskid="Power Check",
    )
