import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):

    run(
        testscript=os.path.join(SCRIPT_PATH, "check_ntp_associations.py"),
        runtime=runtime,
        taskid="Check NTP settings & association",
    )
