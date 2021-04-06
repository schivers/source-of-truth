Sample run

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