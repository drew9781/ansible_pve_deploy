# ansible_pve_deploy

This module uses a yml template to create VM clones on proxmox using ansible and qm command.

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
python3 ansible_pve_deploy/__main__.py template.yml
```
The script takes the yml file as a configuration file for the clones. Edit the file to specify clone information.  
  
To destroy VMs, you can use the same yml file.
```
python3 ansible_pve_deploy template.yml destroy
```

## Prepare template on proxmox
```
wget https://cloud-images.ubuntu.com/bionic/current/bionic-server-cloudimg-amd64.img
qm create 9000 --memory 2048 --net0 virtio,bridge=vmbr0
qm importdisk 9000 bionic-server-cloudimg-amd64.img local-lvm
qm set 9000 --scsihw virtio-scsi-pci --scsi0 local-lvm:vm-9000-disk-1
qm set 9000 --ide2 FreenasImages:cloudinit
qm set 9000  --boot c --bootdisk scsi0
qm template 9000
```

### to-do:  
- ~~convert template format to yaml instead of csv~~  
- ~~Add VM destroyer function~~
