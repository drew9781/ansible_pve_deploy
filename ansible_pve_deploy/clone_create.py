#! /usr/bin/python3 
from ansible_play import ansiblePlay
from qm_format import qm_format
import json
import time
import os

def clone_create(i, ansible_password, ansible_hosts_file, clones, pve, templateID, vmUser, vmPass, vmImage):
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

    if vmImage == True:
        done = False
        while done != True:
            response = os.system("ping -c 1 " + clone_ip)
            if response == 0:
                done = True
            else:
                time.sleep(5)
        print(clone_name + " is pinging!") 
        time.sleep(20)          
        play.ansibleRun(module = 'raw test -e /usr/bin/python || (apt -y update && apt install -y python-minimal)', host =  clone_name, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)


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