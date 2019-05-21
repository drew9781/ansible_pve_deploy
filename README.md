# ansible_pve_deploy

This module uses a csv (yml in future) template to create VM clones on proxmox using ansible and qm command.

edit template.csv to include the clones and information. You must have an existing template. Your proxmox host must also be in you ansible hosts file; the default is pve.

For this to work properly, you must disable ssh strict host key checking.

## Install

```  
git clone github.com/drew9781/ansible_pve_deploy
cd ansible_pve_deploy
pip3 install . 
```  

## Usage
```
python3 ansible_pve_deploy/__main__.py template.csv
```
The script takes the csv file as a configuration file for the clones. Edit the file to specify clone information.


to-do:  
- convert template format to yaml instead of csv  

