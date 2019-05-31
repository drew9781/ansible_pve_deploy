#! /usr/bin/python3
from config_parse import parse_template_yml
from clone_create import clone_create
from clone_destroy import clone_destroy
from getpass import getpass
import time
import sys
from multiprocessing import Process

def main():
    if destroy:
        clone_destroy(i,ansible_password , ansible_hosts_file, clones, pve, templateID, vmUser, vmPass, vmImage)
    else:
        clone_create(i,ansible_password , ansible_hosts_file, clones, pve, templateID, vmUser, vmPass, vmImage)


# Take config file from Arg, and prompt for the Ansible password.
file = sys.argv[1]
ansible_password = getpass(prompt='Ansible sudo password:')
try:
    if sys.argv[2] == "destroy":
        destroy = True
except:
    destroy = False

# parse template for vars
ansible_hosts_file, clones, pve, templateID, vmUser, vmPass, vmImage = parse_template_yml(file)

# for every clone run the qm command
for i in range(len(clones)):
   
   Process(target = main).start()
   time.sleep(5)
   #main()

quit