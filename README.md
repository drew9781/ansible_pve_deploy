# ansible_pve_deploy
work in progress, still needs code clean up

This module uses a template to create VM clones on proxmox using ansible and qm command.

edit template.csv to include the clones and information. You must have an existing template. Your proxmox host must also be in you ansible hosts file; the default is pve.

to-do:  
-convert template format to yaml instead of csv  
-clean up ansibleRun class  
