__author__ = 'racktivity'
from logger import logger

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    fields = ('name', 'id', 'meteringdevicetype', 'meteringdeviceconfigstatus', 'template', 'rackguid', 'parentmeteringdeviceguid', \
              'clouduserguid', 'height', 'positionx', 'positiony', 'positionz', 'attributes', 'tags')

    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    status = q.enumerators.meteringdeviceconfigstatus
    
    previousStatus = meteringdevice.meteringdeviceconfigstatus
    
    changed = False

    for key, value in params.iteritems():
        if key in fields and (value is not None) and value != '':
            setattr(meteringdevice, key, value)
            changed = True
    if params['accounts']:
        for accountdict in params['accounts']:
            if 'guid' in accountdict:
                for account in meteringdevice.accounts:
                    if account.guid == accountdict['guid']:
                        for key, value in accountdict.iteritems():
                            setattr(account, key, value)
        changed = True

    if params["networkinfo"]:
        meteringdevice.network.ipaddress = params["networkinfo"]["ipaddress"]
        meteringdevice.network.port = params["networkinfo"]["port"]
        meteringdevice.network.protocol = params["networkinfo"]["protocol"]
        changed = True

    if changed:
        #logger.log_tasklet(__tags__, params, fields)
        p.api.model.racktivity.meteringdevice.save(meteringdevice)
    params['result'] = {'returncode': True, 'meteringdeviceguid': meteringdevice.guid}
    
def match(q, i, params, tags):
    return True
