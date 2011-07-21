__author__ = 'racktivity'
__priority__= 3
from logger import logger

def main(q, i, p, params, tags):
    #logger.log_tasklet(__tags__, params)
    params['result'] = {'returncode':False}
    deviceguid = params['deviceguid']
    device = p.api.model.racktivity.device.get(deviceguid)
    if len(device.capacityunitsconsumed) > 0 :
        q.eventhandler.raiseError('Device still in use.')
    powerports = device.powerports
    for powerport in powerports:
        if powerport.status == q.enumerators.powerportstatustype.ACTIVE:
            p.api.action.racktivity.device.disconnectPowerPort(deviceguid, powerport.name, powerport.cableguid, request = params["request"])

    result = p.api.model.racktivity.device.delete(deviceguid)
    params['result'] = {'returncode': result}

def match(q, i, params, tags):
    return True
