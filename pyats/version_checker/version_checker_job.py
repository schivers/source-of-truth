import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):

    run(
        testscript=os.path.join(SCRIPT_PATH, "version_checker.py"),
        runtime=runtime,
        taskid="Ensure that the IOS / IOS-XE version matches with the agreed version",
    )
