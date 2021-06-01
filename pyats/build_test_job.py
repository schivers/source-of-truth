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
       testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/version_checker/version_checker.py"),
       runtime=runtime,
       taskid="Version Checker",
     )
    run(
       testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/check_cdp/cdp_enabled.py"),
       runtime=runtime,
       taskid="Check CDP is enabled",
     )
    run(
       testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/check_lldp/check_lldp.py"),
       runtime=runtime,
       taskid="Check LLDP is enabled",
     )
    run(
       testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/check_snmp/check_snmp_settings.py"),
       runtime=runtime,
       taskid="Check SNMP settings",
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/check_dns/check_dns_server_settings.py"),
      runtime=runtime,
      taskid="Check DNS Server Settings",
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/errdisabled/errdisabled.py"),
      runtime=runtime,
      taskid="Check Errdisabled Configuration",
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/check_dns_server_settings/check_dns_server_settings.py"),
      runtime=runtime,
      taskid="Check DNS Server Settings",
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/check_ntp/check_ntp_associations.py"),
      runtime=runtime,
      taskid="Check NTP Settings",
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/local_users/local_user_check.py"),                   
      runtime=runtime,
      taskid="Check Local Users",       
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/remote_management_access/remote_manage.py"),                         
      runtime=runtime,
      taskid="Check Device Management (Hostname, Creds, Domain name, crypto, SSH Version, VTY SSH Input, AAA, Enable secret)",        
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/syslog/check_syslog.py"),                            
      runtime=runtime,
      taskid="Check Syslog)",        
     )
    run(
      testscript=os.path.join(SCRIPT_PATH, "/home/ntt/source-of-truth/pyats/running_vs_startup/run_vs_start.py"),
      runtime=runtime,
     taskid="Compare runnning-config to startup-config",
     )