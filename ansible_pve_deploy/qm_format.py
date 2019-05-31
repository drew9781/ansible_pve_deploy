#! /usr/bin/python3

# Format the QM commands from parse vars on template
def qm_format(arg1, clones, templateID, vmUser, vmPass):
    clone_id =   str(clones[arg1]['id'])
    clone_name = str(clones[arg1]['clone'])
    clone_ip =   str(clones[arg1]['ip'])
    clone_gw =   str(clones[arg1]['gw'])
    templateID = str(templateID)
    vmPass = str(vmPass)
    vmUser = str(vmUser)

    # qm clone FIRSTVMID cloneID --name name
    qmClone = "qm clone " + templateID + " " + clone_id + " --name " + clone_name
    
    # qm set  --ipconfig0 ip=10.0.10.123/24,gw=10.0.10.1
    qmIP = "qm set " + clone_id + " --ipconfig0 'ip="+ clone_ip +",gw=" + clone_gw + "'"
    
    # qm set    --sshkey key --ciuser name
    qmUser = "qm set " + clone_id + ' --sshkey ~/.ssh/id_rsa.pub --ciuser ' + vmUser + ' --cipassword ' + vmPass

    # qm resize    scsi0 +10G
    qmResize= "qm resize " + clone_id + " scsi0 +10G"
    return qmClone, qmIP, clone_name, clone_ip.split('/')[0], clone_id, qmUser, qmResize

def qm_format_destroy(arg1, clones):
    clone_id =   str(clones[arg1]['id'])
    clone_name = str(clones[arg1]['clone'])
    clone_ip =   str(clones[arg1]['ip'])

    qmStop= "qm stop" + clone_id
    qmDestroy= "qm destroy " + clone_id

    return qmStop, qmDestroy, clone_name, clone_ip.split('/')[0]
    