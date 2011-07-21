__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating device properties in the model', 3)
    device = p.api.model.racktivity.device.get(params['deviceguid'])

    fields = ('name', 'devicetype', 'description', 'template', 'rackguid', 'datacenterguid', 'racku', 'racky', 'rackz',
              'modelnr', 'serialnr', 'firmware', 'lastcheck', 'status', 'parentdeviceguid', 'lastrealitycheck', 'tags')
    objectfields = ('components', 'pdisks', 'nicports', 'powerports', 'accounts')
    changed = False

    for key, value in params.iteritems():
        if key in fields and value:
            setattr(device, key, value)
            changed = True
        elif key in objectfields and value:
            objectlist = getattr(device, key)
            for objdata in value:
                newobj = objectlist.new()
                for k, v in objdata.iteritems():
                    setattr(newobj, k, v)
                objectlist.append(newobj)
                changed = True
                
    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.device.save(device)
    
    params['result'] = {'returncode': True,
                        'deviceguid': device.guid}
    
    #import racktivityui.uigenerator.device
    #racktivityui.uigenerator.device.update(device.guid)

def match(q, i, params, tags):
    return True

