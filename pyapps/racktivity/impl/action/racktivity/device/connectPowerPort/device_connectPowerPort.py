__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    portname = params['portname']
    q.logger.log('Disconnect powerport %s' % portname, 3)
    device = p.api.model.racktivity.device.get(params['deviceguid'])
    cableguid = params['cableguid']
    for port in device.powerports:
        if port.name == portname:
            port.cableguid = cableguid
            port.status = q.enumerators.powerportstatustype.ACTIVE
    p.api.model.racktivity.device.save(device)
    
    params['result'] = {'returncode': True,
                        'deviceguid': device.guid}



def match(q, i, params, tags):
    return True

