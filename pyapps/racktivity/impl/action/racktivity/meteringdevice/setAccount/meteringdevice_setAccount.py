__author__ = 'racktivity'
from rootobjectaction_lib import events

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdeviceguid = params['meteringdeviceguid']
    meteringdevice = p.api.model.racktivity.meteringdevice.get(meteringdeviceguid)
    if not meteringdevice.parentmeteringdeviceguid:
        master = meteringdevice
    else:
        master = p.api.model.racktivity.meteringdevice.get(meteringdevice.parentmeteringdeviceguid)

    login = params['login']
    password = params['password']
    usertype = params['usertype']
    #result = p.api.actor.meteringdevice.setConfigurationParameter(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id,
    #                                                                  "AdminLoginAndPassword", login, master.accounts[0].login, master.accounts[0].password)
    result = p.api.actor.meteringdevice.setAccount(master.meteringdevicetype, master.network.ipaddress, master.network.port,
                                                       master.accounts[0].login, master.accounts[0].password,
                                                       login, password, usertype)

    if not result['result']:
        events.raiseError("Failed to set login %s"% master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0076', tags='', escalate=False)
    
    #we save before we continue to make sure that the login of the meteringdeivce is the same as the one in drp
    #so if setting password failed, we still can access the device.
    if (usertype == "admin"):
        master.accounts[0].login = login
        master.accounts[0].password = password
        p.api.model.racktivity.meteringdevice.save(master)
    
    if not result['result']:
        events.raiseError("Failed to set username/password for meteringdevice %s" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0077', tags='', escalate=False)
    
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True
