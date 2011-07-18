__author__ = 'racktivity'
__tags__ = 'device', 'updateModelProperties'
__priority__= 3
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    q.logger.log('Updating device properties in the model', 3)
    device = q.drp.device.get(params['deviceguid'])

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
        logger.log_tasklet(__tags__, params, fields)
        q.drp.device.save(device)
    
    params['result'] = {'returncode': True,
                        'deviceguid': device.guid}
    
    import racktivityui.uigenerator.device
    racktivityui.uigenerator.device.update(device.guid)

def match(q, i, params, tags):
    return True

