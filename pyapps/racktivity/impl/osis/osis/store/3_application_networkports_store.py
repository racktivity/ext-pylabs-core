__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = p.application.getOsisConnection(p.api.appname)
    viewname = '%s_view_%s_networkports' % (params['domain'], params['rootobjecttype'])
    root = params['rootobject']
    records = [] 
    for service in root.networkservices:
        if service.monitor == False:
             servicemonitor = False
        else:
             servicemonitor = True
             
        for networkport in service.ports:
            if root.machineguid:
                fields = {}
                fields['portguid']      = networkport.guid
                fields['portnr']        = networkport.portnr
                fields['machineguid']   = root.machineguid
                fields['ipaddress']     = networkport.ipaddress  
                fields['ipprotocoltype']= str(networkport.ipprotocoltype)
                fields['monitor']       = networkport.monitor
                fields['servicemonitor']= servicemonitor
                records.append(fields)        
    
    osis.viewSave(params['domain'], 'application', viewname, root.guid, root.version, records)
                
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'application'
