Sample run
`
ntt@inspiron-3521:~/ansible$ sudo ansible-playbook cisco-backup.yaml -i nb_inventory.yml --ask-vault-pass
Vault password:

PLAY [Backup all network ios switches] *************************************************************************************************************************************************************
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts
[WARNING]: Ignoring timeout(10) for ios_facts

TASK [Gathering Facts] *****************************************************************************************************************************************************************************
ok: [BAKMTR1SWA01]
[WARNING]: Ignoring timeout(10) for ios_facts
ok: [BAKMTR1SWA02]
ok: [BAKMTR2SWA01]
ok: [BAKMTR2SWA02]
ok: [BAKMTR1SWC02]
ok: [BAKMTR1SWC01]

TASK [show run] ************************************************************************************************************************************************************************************
ok: [BAKMTR2SWA01]
ok: [BAKMTR1SWA01]
ok: [BAKMTR1SWC02]
ok: [BAKMTR1SWA02]
ok: [BAKMTR1SWC01]
ok: [BAKMTR2SWA02]

TASK [save output to /opt/ansible/backups] *********************************************************************************************************************************************************
changed: [BAKMTR2SWA01]
changed: [BAKMTR1SWA02]
changed: [BAKMTR1SWA01]
changed: [BAKMTR1SWC01]
changed: [BAKMTR1SWC02]
changed: [BAKMTR2SWA02]

PLAY RECAP *****************************************************************************************************************************************************************************************
BAKMTR1SWA01               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR1SWA02               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR1SWC01               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR1SWC02               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR2SWA01               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
BAKMTR2SWA02               : ok=3    changed=1    unreachable=0    failed=0    skipped=0    rescued=0    ignored=0
`

`
ntt@inspiron-3521:~/ansible$ cd /opt/ansible/backups/
ntt@inspiron-3521:/opt/ansible/backups$ ll
total 400
drwxr-xr-x 2 root root  4096 Apr  6 12:08 ./
drwxr-xr-x 3 root root  4096 Mar  3 15:24 ../
-rw-r--r-- 1 root root 10387 Mar  3 18:53 BAKMTR1SWA01_20210303-1853.txt
-rw-r--r-- 1 root root  8045 Mar  3 19:18 BAKMTR1SWA01_20210303-1918.txt
-rw-r--r-- 1 root root  8045 Mar  4 11:04 BAKMTR1SWA01_20210304-1103.txt
-rw-r--r-- 1 root root  8045 Mar  4 11:10 BAKMTR1SWA01_20210304-1110.txt
-rw-r--r-- 1 root root  8345 Apr  6 11:52 BAKMTR1SWA01_20210406-1152.txt
-rw-r--r-- 1 root root  8345 Apr  6 11:56 BAKMTR1SWA01_20210406-1156.txt
-rw-r--r-- 1 root root  8345 Apr  6 12:08 BAKMTR1SWA01_20210406-1208.txt
-rw-r--r-- 1 root root 10387 Mar  3 19:18 BAKMTR1SWA02_20210303-1918.txt
-rw-r--r-- 1 root root 10387 Mar  4 11:04 BAKMTR1SWA02_20210304-1103.txt
-rw-r--r-- 1 root root 10387 Mar  4 11:10 BAKMTR1SWA02_20210304-1110.txt
-rw-r--r-- 1 root root 10314 Apr  6 11:52 BAKMTR1SWA02_20210406-1152.txt
-rw-r--r-- 1 root root 10314 Apr  6 11:56 BAKMTR1SWA02_20210406-1156.txt
-rw-r--r-- 1 root root 10314 Apr  6 12:08 BAKMTR1SWA02_20210406-1208.txt
-rw-r--r-- 1 root root 54587 Mar  4 11:10 BAKMTR1SWC01_20210304-1110.txt
-rw-r--r-- 1 root root 60903 Apr  6 12:08 BAKMTR1SWC01_20210406-1208.txt
-rw-r--r-- 1 root root 27418 Apr  6 11:52 BAKMTR1SWC02_20210406-1152.txt
-rw-r--r-- 1 root root 27418 Apr  6 11:56 BAKMTR1SWC02_20210406-1156.txt
-rw-r--r-- 1 root root 27418 Apr  6 12:08 BAKMTR1SWC02_20210406-1208.txt
-rw-r--r-- 1 root root  7783 Apr  6 11:52 BAKMTR2SWA01_20210406-1152.txt
-rw-r--r-- 1 root root  7783 Apr  6 11:56 BAKMTR2SWA01_20210406-1156.txt
-rw-r--r-- 1 root root  7783 Apr  6 12:08 BAKMTR2SWA01_20210406-1208.txt
-rw-r--r-- 1 root root  7835 Apr  6 11:52 BAKMTR2SWA02_20210406-1152.txt
-rw-r--r-- 1 root root  7835 Apr  6 11:56 BAKMTR2SWA02_20210406-1156.txt
-rw-r--r-- 1 root root  7835 Apr  6 12:08 BAKMTR2SWA02_20210406-1208.txt
`