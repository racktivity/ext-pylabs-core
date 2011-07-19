__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_services' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    records = []
    for service in root.services:
        fields = {'name': root.name, 
                  'description': root.description, 
                  'status': root.status, 
                  'template': root.template, 
                  'applicationtemplateguid': root.applicationtemplateguid,
                  'machineguid': root.machineguid, 
                  'customsettings': root.customsettings, 
                  'servicename':'', 
                  'servicedescription':'', 
                  'serviceenabled':''}
        
        fields['servicename']        = service.name
        fields['servicedescription'] = service.description
        fields['serviceenabled']     = service.enabled
        
        q.logger.log ('Looping through all services for application')
        for service2app in service.service2applications:
            fields['service2applicationguid'] = service2app.applicationguid
            records.append(fields)
        
        for service2clouduser in service.service2cloudusers:
            fields['service2clouduserguid'] = service2clouduser.clouduserguid
            records.append(fields)
        
        for service2device in service.service2devices:
            fields['service2deviceguid'] = service2device.deviceguid
            records.append(fields)
        
        for service2disk in service.service2disks:
            fields['service2diskguid'] = service2disk.diskguid
            records.append(fields)
    
        for service2lan in service.service2lans:
            fields['service2languid'] = service2lan.languid
            records.append(fields)
    
        for service2machine in service.service2machines:
            fields['service2machineguid'] = service2machine.machineguid
            records.append(fields)
        
        for service2networkzone in service.service2networkzones:
            fields['service2networkzoneguid'] = service2networkzone.networkzoneguid
            records.append(fields)
        
        for service2resourcegroup in service.service2resourcegroups:
            fields['service2resourcegroupguid'] = service2resourcegroup.resourcegroupguid
            records.append(fields)

    osis.viewSave(params['domain'], 'application', viewname, root.guid, root.version, records)

def match(q, i, params, tags):
    return params['rootobjecttype'] == 'application'
