#! /usr/bin/python3
from ansible_pve_deploy.ansiblePlay import ansiblePlay
from ansible_pve_deploy.qmClone import parse_template, qm_format
from getpass import getpass
import json
import time
import sys
import os

from multiprocessing import Process


cloneVarLength = 5 #How many variables will the template take per clone?
file = sys.argv[1]
ansible_hosts_file = '/etc/ansible/hosts'
ansible_password = getpass(prompt='Ansible sudo password:')

def main():
    qm_clone, qm_ip, clone_name, clone_ip, clone_id, qmUser, qmResize = qm_format(i, clones, templateID, vmUser, vmPass)
    play = ansiblePlay()
    # Clone and configure ip for new VMS on pve host
    play.ansibleRun(module = 'shell ', host =  pve, qm = qm_clone, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)
    play.ansibleRun(module = 'shell ', host =  pve, qm = qm_ip, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)
    if vmUser != 'Username':
        play.ansibleRun(module = 'shell ', host =  pve, qm = qmUser, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)
        play.ansibleRun(module = 'shell ', host =  pve, qm = qmResize, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)
    play.ansibleRun(module = 'shell ', host =  pve, qm = 'qm start '+ clone_id, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)

    # add clones to ansible hosts file
    play.ansibleRun(module = 'lineinfile ', host =  'localhost', args = dict(path=ansible_hosts_file, line=clone_name + ' ansible_host=' + clone_ip, create='yes' ), ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)
    #play.ansibleRun(module = 'shell ', host =  'localhost', args = 'ssh-keygen -f "~/.ssh/known_hosts" -R ' + clone_ip, ansible_hosts_file = ansible_hosts_file)

    if vmImage == "True":
        done = False
        while done != True:
            response = os.system("ping -c 1 " + clone_ip)
            if response == 0:
                done = True
            else:
                time.sleep(5)
        print(clone_name + " is pinging!")            

## install python2
 tasks:
  - name: install python 2
    raw: test -e /usr/bin/python || (apt -y update && apt install -y python-minimal)
    
    else:
        
        #wait for cloudinit to finish
        done = None
        print("Waiting 3 minutes for " + clone_name + " to Boot!")
        time.sleep(180)

        while done != True:
            # play command to check if cloud init finished
            stat = play.ansibleRun(module = 'stat ', host =  clone_name, args = dict(path='/var/lib/cloud/instance/boot-finished'), ansible_hosts_file = ansible_hosts_file, json = True)

            try:
                # run play command and extract json
                play.json = json.loads(stat.json)
                if play.json[clone_name]['stat']['exists'] == False:
                    print(clone_name + ' is not finished!')
                #print(play.json[clone_name]['stat']['exists'], ' ' + clone_name)
                done = play.json[clone_name]['stat']['exists']
            except AttributeError:
                print('failed this time ' + clone_name)
            
            time.sleep(10)
        #reboot server
        play.ansibleRun(module = 'reboot ', host = clone_name, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)

# parse template for vars
clones, pve, templateID, vmUser, vmPass, vmImage = parse_template(file)

# for every clone run the qm command
for i in range(1, (len(clones) +1), cloneVarLength):
   
   Process(target = main).start()
   time.sleep(5)
   #main()

quit