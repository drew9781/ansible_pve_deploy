#! /usr/bin/python3
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
        return _ansible_host_file, clones, _ansible_host_address, _template_id
    else:
        return _ansible_host_file, clones, _ansible_host_address, _template_id, _vm_username, _vm_password, _cloud_image
