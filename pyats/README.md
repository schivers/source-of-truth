#PyATS - Python Automated Test Scripts
PyATS uses a testbed file that describes the test environment. Netbox can be used as the source to generate a testbed file and a filter can be used to refine the device list returned by Netbox.
The query filter is simply the URI that appears after the '&' wehn using the search function in the Netbox GUI.

First we need to set up the environment variables. I have save these into src_env so all we need to do is 'source' the variables
```
cd ~/
source src_env
```

Now we can create the testbed.yaml file. The following example will create a testbed.yaml containing all devices with a role of access, distribution or core and includes the topology connections.
Note: This may take a while to complete. You can speed up the task by removing the --topology from the end of the command line.
```
cd pyats
pyats create testbed netbox --output testbed.yaml --netbox-url=${NETBOX_URL} --user-token=${NETBOX_TOKEN} --def_user=admin --def_pass=3uro2o2o --url_filter='q=&status=active&role=access&role=core&role=distribution&mac_address=&has_primary_ip=&local_context_data=&virtual_chassis_member=&console_ports=&console_server_ports=&power_ports=&power_outlets=&interfaces=&pass_through_ports=' --topology
```
Issue: Currently need to manually add BAKMTR2SWC01 and BAKMTR2SWC02 to the testbed.

## Device State
PyATS can be used to capture a device state which is useful for comparison. i.e. Capture the device state day1 and again day2. Compare the two states and generate a report on the differences. Genie (PyATS) will doo all this for you.

The following learns the state of just BAKMTR1SWC01 in the testbed and saves the information in /learn-20210412-before. Running against the whole stadium network will likley take about >1h to complete.
```
genie learn all --devices BAKMTR1SWC01 --testbed-file testbed.yaml --output learn-20210412-before
```

Run the command again
```
genie learn all --devices BAKMTR1SWC01 --testbed-file testbed.yaml --output learn-20210412-after
```

Run the diff script to report on the differences
```
genie diff learn-20210412 learn-20210412-after 20210412-diff
```

## PyATS Job File
The recomended way to run a series of tests is to complie the tests into a job file and then run the job file as follows. 
```
easypy Baku_test_job.py -html_logs PyATS-Reports -testbed_file testbed.yaml
```

A sample output from running the job file with just the hostname checker.py test
```
2021-04-12T14:05:36: %EASYPY-INFO: Generating HTML report file
2021-04-12T14:05:37: %EASYPY-INFO: --------------------------------------------------------------------------------
2021-04-12T14:05:37: %EASYPY-INFO: Job finished. Wrapping up...
2021-04-12T14:05:37: %EASYPY-INFO: Creating archive file: /home/ntt/.pyats/archive/21-Apr/Baku_test_job.2021Apr12_14:00:27.054192.zip
2021-04-12T14:05:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2021-04-12T14:05:37: %EASYPY-INFO: |                                Easypy Report                                 |
2021-04-12T14:05:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2021-04-12T14:05:37: %EASYPY-INFO: pyATS Instance   : /usr
2021-04-12T14:05:37: %EASYPY-INFO: Python Version   : cpython-3.6.9 (64bit)
2021-04-12T14:05:37: %EASYPY-INFO: CLI Arguments    : /home/ntt/.local/bin/easypy Baku_test_job.py -html_logs Reports_20210412 -testbed_file testbed.yaml
2021-04-12T14:05:37: %EASYPY-INFO: User             : ntt
2021-04-12T14:05:37: %EASYPY-INFO: Host Server      : inspiron-3521
2021-04-12T14:05:37: %EASYPY-INFO: Host OS Version  : Ubuntu 18.04 bionic (x86_64)
2021-04-12T14:05:37: %EASYPY-INFO:
2021-04-12T14:05:37: %EASYPY-INFO: Job Information
2021-04-12T14:05:37: %EASYPY-INFO:     Name         : Baku_test_job
2021-04-12T14:05:37: %EASYPY-INFO:     Start time   : 2021-04-12 14:00:37.635920
2021-04-12T14:05:37: %EASYPY-INFO:     Stop time    : 2021-04-12 14:05:36.832456
2021-04-12T14:05:37: %EASYPY-INFO:     Elapsed time : 299.196536
2021-04-12T14:05:37: %EASYPY-INFO:     Archive      : /home/ntt/.pyats/archive/21-Apr/Baku_test_job.2021Apr12_14:00:27.054192.zip
2021-04-12T14:05:37: %EASYPY-INFO:
2021-04-12T14:05:37: %EASYPY-INFO: Total Tasks    : 2
2021-04-12T14:05:37: %EASYPY-INFO:
2021-04-12T14:05:37: %EASYPY-INFO: Overall Stats
2021-04-12T14:05:37: %EASYPY-INFO:     Passed     : 2
2021-04-12T14:05:37: %EASYPY-INFO:     Passx      : 0
2021-04-12T14:05:37: %EASYPY-INFO:     Failed     : 1
2021-04-12T14:05:37: %EASYPY-INFO:     Aborted    : 0
2021-04-12T14:05:37: %EASYPY-INFO:     Blocked    : 0
2021-04-12T14:05:37: %EASYPY-INFO:     Skipped    : 0
2021-04-12T14:05:37: %EASYPY-INFO:     Errored    : 0
2021-04-12T14:05:37: %EASYPY-INFO:
2021-04-12T14:05:37: %EASYPY-INFO:     TOTAL      : 3
2021-04-12T14:05:37: %EASYPY-INFO:
2021-04-12T14:05:37: %EASYPY-INFO: Success Rate   : 66.67 %
2021-04-12T14:05:37: %EASYPY-INFO:
2021-04-12T14:05:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2021-04-12T14:05:37: %EASYPY-INFO: |                             Task Result Summary                              |
2021-04-12T14:05:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2021-04-12T14:05:37: %EASYPY-INFO: Validate Connectivity to Testsbed Devices: testbed_connectivity.com...    PASSED
2021-04-12T14:05:37: %EASYPY-INFO: Validate Connectivity to Testsbed Devices: testbed_connectivity.ver...    FAILED
2021-04-12T14:05:37: %EASYPY-INFO: Validate Connectivity to Testsbed Devices: testbed_connectivity.com...    PASSED
2021-04-12T14:05:37: %EASYPY-INFO:
2021-04-12T14:05:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2021-04-12T14:05:37: %EASYPY-INFO: |                             Task Result Details                              |
2021-04-12T14:05:37: %EASYPY-INFO: +------------------------------------------------------------------------------+
2021-04-12T14:05:37: %EASYPY-INFO: Validate Connectivity to Testsbed Devices: testbed_connectivity
2021-04-12T14:05:37: %EASYPY-INFO: |-- common_setup                                                          PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |   `-- connect                                                           PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |-- verify_connected                                                      FAILED
2021-04-12T14:05:37: %EASYPY-INFO: |   `-- test                                                              FAILED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 1: Test Connection Status of BAK1DSWA01                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 2: Test Connection Status of BAK1DSWA02                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 3: Test Connection Status of BAK1JSWA01                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 4: Test Connection Status of BAK1JSWA02                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 5: Test Connection Status of BAK2ASWA01                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 6: Test Connection Status of BAK2BSWA01                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 7: Test Connection Status of BAK2CSWA01                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 8: Test Connection Status of BAK2DSWA01                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 9: Test Connection Status of BAK2GSWA01                  PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 10: Test Connection Status of BAK2HSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 11: Test Connection Status of BAK2JSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 12: Test Connection Status of BAK4GSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 13: Test Connection Status of BAK4GSWA02                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 14: Test Connection Status of BAK4ISWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 15: Test Connection Status of BAK4ISWA02                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 16: Test Connection Status of BAK4JSWA02                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 17: Test Connection Status of BAKGA1SWA01                PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 18: Test Connection Status of BAKGA1SWA02                PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 19: Test Connection Status of BAKGA3SWA01                PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 20: Test Connection Status of BAKGA3SWA02                PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 21: Test Connection Status of BAKGASWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 22: Test Connection Status of BAKGASWA02                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 23: Test Connection Status of BAKGBSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 24: Test Connection Status of BAKGBSWA02                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 25: Test Connection Status of BAKGCSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 26: Test Connection Status of BAKGDSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 27: Test Connection Status of BAKGFSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 28: Test Connection Status of BAKGGSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 29: Test Connection Status of BAKGHSWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 30: Test Connection Status of BAKGISWA01                 PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 31: Test Connection Status of BAKMTR1SWA01               PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 32: Test Connection Status of BAKMTR1SWA02               PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 33: Test Connection Status of BAKMTR1SWC01               FAILED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 34: Test Connection Status of BAKMTR1SWC02               FAILED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 35: Test Connection Status of BAKMTR2SWC01               FAILED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 36: Test Connection Status of BAKMTR2SWC02               FAILED
2021-04-12T14:05:37: %EASYPY-INFO: |       |-- STEP 37: Test Connection Status of BAKMTR2SWA01               PASSED
2021-04-12T14:05:37: %EASYPY-INFO: |       `-- STEP 38: Test Connection Status of BAKMTR2SWA02               PASSED
2021-04-12T14:05:37: %EASYPY-INFO: `-- common_cleanup                                                        PASSED
2021-04-12T14:05:37: %EASYPY-INFO: Check Configured Hostname: hostname_checker
2021-04-12T14:05:37: %EASYPY-INFO: Sending report email...
2021-04-12T14:05:37: %EASYPY-INFO: Missing SMTP server configuration, or failed to reach/authenticate/send mail. Result notification email failed to send.
2021-04-12T14:05:37: %EASYPY-INFO: Done!

Pro Tip
-------
   Try the following command to view your logs:
       pyats logs view
```

PyATS will write a dated .zip report to /home/ntt/.pyats/archive/ and a non-dated html file to /PyATS-Reports

## Test files

*  ***hostname_checker.py*** - Checks each device's configured hostname against that defined in the testbed.yaml
*  ***interface_errors.py*** - Checks each interface in the testbed.yaml for errors
*  ***interface_snmp_linkstatus.py*** 
*  ***version_checker.py*** - checks the IOS version against a hardcoded value within the script