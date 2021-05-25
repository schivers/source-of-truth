import os
from pyats.easypy import run

# compute the script path from this location
SCRIPT_PATH = os.path.dirname(__file__)


def main(runtime):
    """job file entrypoint"""

    # run script
    run(
        testscript=os.path.join(SCRIPT_PATH, "run_vs_start.py"),
        runtime=runtime,
        taskid="Running vs. Startup",
    )
