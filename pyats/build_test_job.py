"""
 build_test_job.py
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
        testscript=os.path.join(SCRIPT_PATH, "./version_checker/version_checker.py"),
        runtime=runtime,
        taskid="Version Checker",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./cdp_enabled/cdp_enabled.py"),
        runtime=runtime,
        taskid="Check CDP is enabled per interface",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./cdp_enabled_globally/cdp_enabled_globally.py"),
        runtime=runtime,
        taskid="Check CDP is enabled globally",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./check_lldp/check_lldp.py"),
        runtime=runtime,
        taskid="Check LLDP is enabled",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./check_snmp/check_snmp_settings.py"),
        runtime=runtime,
        taskid="Check SNMP settings",
    )
    run(
        testscript=os.path.join(
            SCRIPT_PATH, "./check_dns/check_dns_server_settings.py"
        ),
        runtime=runtime,
        taskid="Check DNS Server Settings",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./errdisabled/errdisabled.py"),
        runtime=runtime,
        taskid="Check Errdisabled Configuration",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./check_ntp/check_ntp_associations.py"),
        runtime=runtime,
        taskid="Check NTP Settings",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./local_users/local_user_check.py"),
        runtime=runtime,
        taskid="Check Local Users",
    )
    run(
        testscript=os.path.join(
            SCRIPT_PATH, "./remote_management_access/remote_manage.py"
        ),
        runtime=runtime,
        taskid="Check Device Management (Hostname, Creds, Domain name, crypto, SSH Version, VTY SSH Input, AAA, Enable secret)",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./syslog/check_syslog.py"),
        runtime=runtime,
        taskid="Check Syslog",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./running_vs_startup/run_vs_start.py"),
        runtime=runtime,
        taskid="Compare running-config to startup-config",
    )
    run(
        testscript=os.path.join(SCRIPT_PATH, "./show_mls_qos/show_mls_qos.py"),
        runtime=runtime,
        taskid="Check mls_qos is in Config",
    )
    runtime.mail_report.contents.insert('NTT Links',"Log viewer - http://172.26.232.11:8005/results \nNetbox - http://172.26.232.11:8000/ \nBackups - http://172.26.232.11:8008/ ", position=0)

