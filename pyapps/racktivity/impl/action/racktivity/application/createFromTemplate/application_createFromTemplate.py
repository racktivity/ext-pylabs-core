__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    template                    = p.api.model.racktivity.application.get(params['applicationtemplateguid'])
    application                 = p.api.model.racktivity.application.new()
    
    fields = ('deviceguid', 'name', 'description', 'customsettings', 'parentapplicactionguid', 'meteringdeviceguid', 'applicationtemplateguid')
              

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(application, key, value)

    application.template        = False
    application.status          = q.enumerators.applicationstatustype.ACTIVE
    
    for account in template.accounts:
        account.guid = account.version = ''
        application.accounts.append(account)
    
    for service in template.services:
        for service2device in service.service2devices:
            service2device.guid = service2device.version = ''
        for service2application in service.service2applications:
            service2application.guid = service2application.version = ''
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
        application.services.append(service)


    for networkservice in template.networkservices:
        for port in networkservice.ports:
            port.ipaddress = p.api.action.racktivity.machine.getManagementIpaddress(params['machineguid'], includevirtual=False, request = params["request"])['result']
            port.guid = port.version = ''
            
        networkservice.guid = networkservice.version = ''
        application.networkservices.append(networkservice)

    if template.qpackages: application.qpackages = template.qpackages
    if template.configuration: application.configuration = template.configuration

    p.api.model.racktivity.application.save(application)    
    params['result'] = {'returncode':True, 'applicationguid': application.guid}

def match(q, i, params, tags):
    return True
