# ansible_pve_deploy

This module uses a template to create VM clones on proxmox using ansible and qm command.

edit template.csv to include the clones and information. You must have an existing template. Your proxmox host must also be in you ansible hosts file; the default is pve.
