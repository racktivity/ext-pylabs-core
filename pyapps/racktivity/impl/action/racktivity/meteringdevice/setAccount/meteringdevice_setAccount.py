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

    from rootobjectaction_lib import rootobjectaction_find
    applications = rootobjectaction_find.application_find(meteringdeviceguid=master.guid, name='MeteringdeviceAPI')
    masteripaddress = None
    deviceapiport = 0
    if applications:
        application = p.api.model.racktivity.racktivity_application.get(applications[0])
        service = application.networkservices[0]
        ipaddress = p.api.model.racktivity.ipaddress.get(service.ipaddressguids[0])
        masteripaddress = ipaddress.address
        deviceapiport = service.ports[0].portnr
    else:
        events.raiseError("Can't find application with meteringdeviceguid '%s'" % master.guid, messageprivate='', typeid='RACTKVITIY-MON-GENERIC-0030', tags='', escalate=False)

    login = params['login']
    password = params['password']
    usertype = params['usertype']
    #result = q.actions.actor.meteringdevice.setConfigurationParameter(meteringdeviceguid, master.meteringdevicetype, masteripaddress, deviceapiport, meteringdevice.id,
    #                                                                  "AdminLoginAndPassword", login, master.accounts[0].login, master.accounts[0].password)
    result = q.actions.actor.meteringdevice.setAccount(master.meteringdevicetype, masteripaddress, deviceapiport,
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