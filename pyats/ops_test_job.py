"""
ops_test_job.py
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
from pyats.easypy.email import TextEmailReport
from pyats import easypy

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):

    """job file entrypoint"""

    # run script
    run(
        testscript=os.path.join(SCRIPT_PATH, "./testbed_connectivity.py"),
        runtime=runtime,
        taskid="Validate Connectivity",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./check_ntp/check_ntp_associations.py"),
        runtime=runtime,
        taskid="Check NTP Associations",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./eigrp/eigrp.py"),
        runtime=runtime,
        taskid="Check EIGRP Adjacencies",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./half_duplex/half_duplex.py"),
        runtime=runtime,
        taskid="Check for Half Duplex Interfaces ",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./interface_errors/interface_errors.py"),
        runtime=runtime,
        taskid="Check for Interface Errors",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./ping_central_ntp/ping_central_ntp.py"),
        runtime=runtime,
        taskid="Ping IBC NTP Server",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./show_env_all/show_env.py"),
        runtime=runtime,
        taskid="Validate Environment Temp/Fan/Power",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./show_power/show_power.py"),
        runtime=runtime,
        taskid="Checking remaining Power",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./show_proc_cpu/show_proc_cpu.py"),
        runtime=runtime,
        taskid="Check CPU processes",
    )
    runtime.mail_report.contents.insert(
        "NTT Links",
        "Log viewer - http://172.26.232.11:8005/results \nNetbox - http://172.26.232.11:8000/ \nBackups - http://172.26.232.11:8008/ ",
        position=0,
    )
