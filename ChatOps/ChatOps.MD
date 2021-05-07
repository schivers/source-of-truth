### ChatOps using Cisco Webex Teams
Each script PyATS and Ansible script should post a message into my Cisco Webex Teams bot room with an indication of completion and a useful link to where further information can be found.  

Install the webex teams Ansible from Galaxy
https://docs.ansible.com/ansible/latest/collections/community/general/cisco_webex_module.html
```
ansible-galaxy collection install community.general
```

##Writing out to Webex
I am using a play to write a message to Webex. the following play indicates the start of a 'Config PUSH'
```
---
- hosts: localhost
  connection: local
  gather_facts: False
  vars:
    token: OTBlNDk4NTctMWMwZC00MzE1LWEwOWItYmJkNWU5MjAzZWNiODMzNDE1OTAtOGEz_PF84_0198f08a-3880-4871-b55e-4863ccf723d5
    room_id: Y2lzY29zcGFyazovL3VzL1JPT00vNTIxOWRiYTAtYWNiMC0xMWViLTgzYjctOTVlMTRhZTBhYTE3

  tasks:

     - name: Cisco Webex Teams - Text Message to a Room
       community.general.cisco_webex:
         recipient_type: roomId
         recipient_id: "{{ room_id }}"
         msg_type: text
         personal_token: "{{ token }}"
         msg: "The Baku Device Config PUSH has STARTED"
```

There is a similar play with different words to indicate the COMPLETION of the config push.

Pull it all together into a master playbook as follows
```
# run with sudo ansible-playbook push-update-play.yaml -i nb_inventory.yaml --vault-password-file ~/.vault_pass.txt
- include: push_start_webex_bot.yaml
- include: config_update_v105b1.yaml
- include: push_completed_webex_bot.yaml
```

## References:
* https://developer.webex.com/docs/bots
* https://mayanknauni.com/?p=4335
* https://github.com/mayanknauni/Ansible_HealthCheck_BoT/blob/master/ACI_Controller_Health.yml
* https://docs.ansible.com/ansible/latest/collections/community/general/cisco_webex_module.html
