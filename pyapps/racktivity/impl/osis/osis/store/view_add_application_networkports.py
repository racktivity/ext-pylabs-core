__author__ = 'Incubaid'

def main(q, i, p, params, tags):
    osis = OsisDB().getConnection('main')
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
    
    osis.viewSave('racktivity_application', 'view_racktivity_application_networkports', root.guid, root.version, records)
                
    
def match(q, i, params, tags):
    return params['rootobjecttype'] == 'racktivity_application'
