#! /usr/bin/python3 
from ansible_play import ansiblePlay
from qm_format import qm_format_destroy


def clone_destroy(i, ansible_password, ansible_hosts_file, clones, pve, templateID, vmUser, vmPass, vmImage):
    qmStop, qmDestroy, clone_name, clone_ip = qm_format_destroy(i, clones)
    play = ansiblePlay()
    
    play.ansibleRun(module = 'shell ', host =  pve, qm = qmStop, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)
    play.ansibleRun(module = 'shell ', host =  pve, qm = qmDestroy, ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)


    # remove clones from ansible hosts file
    play.ansibleRun(module = 'lineinfile ', host =  'localhost', args = dict(path=ansible_hosts_file, line=clone_name + ' ansible_host=' + clone_ip, state='absent' ), ansible_hosts_file = ansible_hosts_file, ansible_password = ansible_password)
