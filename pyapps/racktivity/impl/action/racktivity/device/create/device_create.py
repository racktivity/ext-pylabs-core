__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    q.logger.log('Creating the new device in the model', 3)
    device = p.api.model.racktivity.device.new()
    fields = ('name', 'devicetype', 'description', 'template', 'rackguid', 'datacenterguid', 'racku', 'racky', 'rackz', 'modelnr', 'serialnr', 'firmware',
               'lastcheck', 'status', 'parentdeviceguid', 'lastrealitycheck', 'tags')
    objectfields = ('components', 'pdisks', 'nicports', 'powerports', 'accounts')
    
    for key, value in params.iteritems():
        if key in fields and value:
            setattr(device, key, value)
        elif key in objectfields and value:
            objectlist = getattr(device, key)
            for objdata in value:
                newobj = objectlist.new()
                for k, v in objdata.iteritems():
                    setattr(newobj, k, v)
                objectlist.append(newobj)
    acl = device.acl.new()
    device.acl = acl
    p.api.model.racktivity.device.save(device)

    #from rootobjectaction_lib import rootobject_grant
    #rootobject_grant.grantUser(device.guid, 'device', params['request']['username'])

    params['result'] = {'returncode': True, 'deviceguid': device.guid}
    
    #if params['rackguid']:
        #import racktivityui.uigenerator.device
        #racktivityui.uigenerator.device.create(device.guid, params['rackguid'])
        
        #import racktivityui.uigenerator.rack
        #racktivityui.uigenerator.rack.update(params['rackguid'])

def match(q, i, params, tags):
    return True
