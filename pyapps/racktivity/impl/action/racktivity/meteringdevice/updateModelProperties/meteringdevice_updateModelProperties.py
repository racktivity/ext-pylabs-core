__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'updateModelProperties'
from logger import logger

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    fields = ('name', 'id', 'meteringdevicetype', 'meteringdeviceconfigstatus', 'template', 'rackguid', 'parentmeteringdeviceguid', \
              'clouduserguid', 'height', 'positionx', 'positiony', 'positionz', 'attributes', 'tags')

    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    status = q.enumerators.meteringdeviceconfigstatus
    
    previousStatus = meteringdevice.meteringdeviceconfigstatus
    
    changed = False

    for key, value in params.iteritems():
        if key in fields and (value is not None) and value != '':
            setattr(meteringdevice, key, value)
            changed = True
    if 'accounts' in params and params['accounts']:
        for accountdict in params['accounts']:
            if 'guid' in accountdict:
                for account in meteringdevice.accounts:
                    if account.guid == accountdict['guid']:
                        for key, value in accountdict.iteritems():
                            setattr(account, key, value)
        changed = True

    if changed:
        logger.log_tasklet(__tags__, params, fields)
        q.drp.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True, 'meteringdeviceguid': meteringdevice.guid}
    
    if meteringdevice.meteringdeviceconfigstatus in (status.CONFIGURED, status.USED):
        import racktivityui.uigenerator.meteringdevice
        if previousStatus == status.IDENTIFIED:
            if not meteringdevice.parentmeteringdeviceguid:
                #The device was in the identified state and now it's in the Configured/Used state
                #we also only create a page for the master metering device
                #assuming the rackguid is set correctly
                racktivityui.uigenerator.meteringdevice.create(meteringdevice.guid, meteringdevice.rackguid)
        else:
            racktivityui.uigenerator.meteringdevice.update(meteringdevice.parentmeteringdeviceguid if meteringdevice.parentmeteringdeviceguid else meteringdevice.guid)
        import racktivityui.uigenerator.rack
        racktivityui.uigenerator.rack.update(meteringdevice.rackguid)

def match(q, i, params, tags):
    return True
