@metadata title=Configuration File
@metadata tagstring=configuration file config xmpp agent


# Configuration File for XMPP Agent

On agent, stored in `/opt/qbase5/cfg/qconfig/agent.cfg`

    [main]
    agentname=$agentname
    password=$password
    domain=$domain
    agentcontrollername=$agentcontrollername
    enable_cron=$True/False
    cron_interval=$cron_interval
    
    [IP_0] # e.g [192_168_96_123]
    registered=$True/False
    subscribed=$True/False
    
    [IP_1]
    registered=$True/False
    subscribed=$True/False
    
    ...
    
    [IP_N] 
    registered=$True/False
    subscribed=$True/False
    
    
    
    [security_$nr] # this part of configuration file is not implemented yet
    agentfilters=*@superadmin.eur.daas.com,*@cloud1.ghent.goodguys.com
    shellcmd=1,1  #$allowed=1,$askpermission=1  #if permission not mentioned than 0
    qshellcmd=1
    portforward=1
    qpackage=1
    agentconnectwith=1
    download=1
    upload=1
    fs=1
    qbasereinstall=1
    dialog=1
    taskbar=1
    rdp=1
    fileread=1
    filewrite=1
    fsdelete=1
    perm=1
    agent = 1
    systemservice=1
    systempasswd=1
    systemreboot=1
