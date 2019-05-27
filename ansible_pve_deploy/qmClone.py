#! /usr/bin/python3
# This reads user input from the specified csv file
import yaml

def parse_template_yml(arg1):
    with open("template.yml", 'r') as F:
        yml = yaml.safe_load(F)

    ## parse required info
    if 'ansible_host_file' in yml:
        _ansible_host_file = yml.get('ansible_host_file')
    else:
        raise Exception('yml config should include ansible_host_file variable, which specifies the ansible inventory file on client.')
    if 'ansible_host_address' in yml:
        _ansible_host_address = yml.get('ansible_host_address')
    else:
        raise Exception('yml config should include ansible_host_address variable, which specifies the proxmox IP/DNS address. ')
    if 'template_id' in yml:
        _template_id = yml.get('template_id')
    else:
        raise Exception('yml config should include template_id variable, which specifies the VM ID on the proxmox host to be used as a template for clones.')

    ## parse optional info
    if 'vm_username' in yml:
        _vm_username = yml.get('vm_username')
    if 'vm_password' in yml:
        _vm_password = yml.get('vm_password')
    if 'cloud_image' in yml:
        _cloud_image = yml.get('cloud_image')
    else:
        _cloud_image = False

    clones = yml['clones']

    if _cloud_image == False:    
        return clones, _ansible_host_address, _template_id
    else:
        return clones, _ansible_host_address, _template_id, _vm_username, _vm_password, _cloud_image



# Format the QM commands from parse vars on template
def qm_format(arg1, clones, templateID, vmUser, vmPass):
    clone_id =   clones[arg1]['id']
    clone_name = clones[arg1]['clone']
    clone_ip =   clones[arg1]['ip']
    clone_gw =   clones[arg1]['gw']
    
    # qm clone FIRSTVMID cloneID --name name
    qmClone = "qm clone " + templateID + " " + clone_id + " --name " + clone_name
    
    # qm set  --ipconfig0 ip=10.0.10.123/24,gw=10.0.10.1
    qmIP = "qm set " + clone_id + " --ipconfig0 'ip="+ clone_ip +",gw=" + clone_gw + "'"
    
    # qm set    --sshkey key --ciuser name
    qmUser = "qm set " + clone_id + ' --sshkey ~/.ssh/id_rsa.pub --ciuser ' + vmUser + ' --cipassword ' + vmPass

    # qm resize    scsi0 +10G
    qmResize= "qm resize " + clone_id + " scsi0 +10G"
    return qmClone, qmIP, clone_name, clone_ip, clone_id, qmUser, qmResize