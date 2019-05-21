#! /usr/bin/python3
# This reads user input from the specified config file
def parse_template(arg1):
    clone = {}
    with open(arg1) as F:
        for i, line in enumerate(F):
            if i == 0:
                #ansible hostname file config
                1 == 1
            elif i == 1: ## get ansible pve hostname
                pve= line.split(",")[1]
                print(pve)
            elif i == 2: ## get templateVM id
                templateID= line.split(',')[1]
            elif i == 3: ## get username for vm
                vmUser= line.split(',')[1]
            elif i == 4: ## get pass for username
                vmPass= line.split(',')[1]
            elif i == 5: ## get ssh key
                vmSSH= line.split(',')[1]
            elif i >= 7: ## get cloneVM info
                # orders the clone's info in a dict, in 5 unit increments
                j = (i-6) *5
                clone[j-4]= line.split(',')[0]
                clone[j-3]= line.split(',')[1]
                clone[j-2]= line.split(',')[2]
                clone[j-1]= line.split(',')[3]
                clone[j  ]= (line.split(',')[4]).rstrip()
    return clone, pve, templateID, vmUser, vmPass, vmSSH

# Format the QM commands from parse vars on template
def qm_format(arg1, clone, templateID, vmUser, vmSSH):
    # qm clone FIRSTVMID cloneID --name name
    clone_id =  clone[arg1 +1]
    clone_name = clone[arg1]
    clone_ip = clone[arg1+2]
    qmClone = "qm clone " + templateID + " " + clone_id + " --name " + clone_name
    
    # qm set  --ipconfig0 ip=10.0.10.123/24,gw=10.0.10.1
    qmIP = "qm set " + clone_id + " --ipconfig0 'ip="+ clone_ip + "/" + clone[arg1+3] + ",gw=" + clone[arg1+4] + "'"
    
    # qm set    --sshkey key --ciuser name
    qmUser = "qm set " + clone_id + ' --sshkey ~/.ssh/is_rsa.pub --ciuser ' + vmUser

    return qmClone, qmIP, clone_name, clone_ip, clone_id, qmUser