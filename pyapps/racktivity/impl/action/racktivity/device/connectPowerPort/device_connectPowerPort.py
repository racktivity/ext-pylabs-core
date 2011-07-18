__author__ = 'racktivity'
__tags__ = 'device', 'connectPowerPort'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    portname = params['portname']
    q.logger.log('Disconnect powerport %s' % portname, 3)
    device = q.drp.device.get(params['deviceguid'])
    cableguid = params['cableguid']
    for port in device.powerports:
        if port.name == portname:
            port.cableguid = cableguid
            port.status = q.enumerators.powerportstatustype.ACTIVE
    q.drp.device.save(device)
    
    params['result'] = {'returncode': True,
                        'deviceguid': device.guid}
    
    import racktivityui.uigenerator.device
    racktivityui.uigenerator.device.update(device.guid)

def match(q, i, params, tags):
    return True

