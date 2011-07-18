__author__ = 'racktivity'
__tags__ = 'racktivity_application', 'createFromTemplate'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    template                    = q.drp.racktivity_application.get(params['applicationtemplateguid'])
    racktivity_application                 = q.drp.racktivity_application.new()
    
    fields = ('deviceguid', 'name', 'description', 'customsettings', 'parentapplicactionguid', 'meteringdeviceguid', 'applicationtemplateguid')
              

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(racktivity_application, key, value)

    racktivity_application.template        = False
    racktivity_application.status          = q.enumerators.applicationstatustype.ACTIVE
    
    for account in template.accounts:
        account.guid = account.version = ''
        racktivity_application.accounts.append(account)
    
    for service in template.services:
        for service2device in service.service2devices:
            service2device.guid = service2device.version = ''
        for service2racktivity_application in service.service2applications:
            service2racktivity_application.guid = service2racktivity_application.version = ''
        for service2lan in service.service2lans:
            service2lan.guid = service2lan.version = ''
        for service2networkzone in service.service2networkzones:
            service2networkzone.guid = service2networkzone.version = ''
        for service2machine in service.service2machines:
            service2machine.guid = service2machine.version = ''
        for service2disk in service.service2disks:
            service2disk.guid = service2disk.version = ''          
        for service2clouduser in service.service2cloudusers:
            service2clouduser.guid = service2clouduser.version = ''
            
        service.guid = service.version = ''
        racktivity_application.services.append(service)


    for networkservice in template.networkservices:
        for port in networkservice.ports:
            port.ipaddress = q.actions.rootobject.machine.getManagementIpaddress(params['machineguid'], includevirtual=False, request = params["request"])['result']
            port.guid = port.version = ''
            
        networkservice.guid = networkservice.version = ''
        racktivity_application.networkservices.append(networkservice)

    if template.qpackages: racktivity_application.qpackages = template.qpackages
    if template.configuration: racktivity_application.configuration = template.configuration

    q.drp.racktivity_application.save(racktivity_application)    
    params['result'] = {'returncode':True, 'applicationguid': racktivity_application.guid}

def match(q, i, params, tags):
    return True
