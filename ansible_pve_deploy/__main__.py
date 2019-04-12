#! /usr/bin/python
from ansible_pve_deploy.ansiblePlay import ansiblePlay
from ansible_pve_deploy.qmClone import parse_template, qm_format
from getpass import getpass
import json
import time
import sys

from multiprocessing import Process


cloneVarLength = 5 #How many variables will the template take per clone?
file = sys.argv[1]
ansible_host_file = '/etc/ansible/hosts'
ansible_password = getpass(prompt='Ansible sudo password:')

def main():
    qm_clone, qm_ip, clone_name, clone_ip, clone_id = qm_format(i, clones, templateID)
    play = ansiblePlay()
    # Clone and configure ip for new VMS on pve host
    play.ansibleRunBecome('shell ', pve, qm_clone, '', ansible_host_file, ansible_password)
    play.ansibleRunBecome('shell ', pve, qm_ip, '', ansible_host_file, ansible_password)
    play.ansibleRunBecome('shell ', pve, 'qm start '+ clone_id, '', ansible_host_file, ansible_password)
    # add clones to ansible hosts file
    play.ansibleRunBecome('lineinfile ', 'localhost', '', dict(path=ansible_host_file, line=clone_name + ' ansible_host=' + clone_ip, create='yes' ), ansible_host_file, ansible_password )
    play.ansibleRun('shell ', 'localhost', 'ssh-keygen -f "~/.ssh/known_hosts" -R ' + clone_ip, '', ansible_host_file)
    #wait for cloudinit to finish
    done = None
    while done != True:
        # play command to check if cloud init finished
        stat = play.ansibleRunJson('stat ', clone_name, '', dict(path='/var/lib/cloud/instance/boot-finished'),ansible_host_file)
        try:
            # run play command and extract json
            play.json = json.loads(stat.json)
            print(play.json[clone_name]['stat']['exists'], ' ' + clone_name)
            done = play.json[clone_name]['stat']['exists']
        except AttributeError:
            print('failed this time ' + clone_name)
        
        time.sleep(5)
    #reboot server
    play.ansibleRunBecome('reboot', clone_name, '', '', ansible_host_file, ansible_password)

# parse template for vars
clones, pve, templateID = parse_template(file)

# for every clone run the qm command
for i in range(1, (len(clones) +1), cloneVarLength):
   
   Process(target = main).start()
   #time.sleep(5)
   #main()

quit