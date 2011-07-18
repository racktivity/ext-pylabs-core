__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'deleteThreshold'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = q.drp.meteringdevice.get(params['meteringdeviceguid'])
    thresholdguid = params['thresholdguid']
    found = False
    for sensor in meteringdevice.sensors:
        if thresholdguid in sensor.thresholdguids:
            sensor.thresholdguids.remove(thresholdguid)
            q.drp.meteringdevice.save(meteringdevice)
            found = True
            break
    if not found:
        for poweroutput in meteringdevice.poweroutputs:
            if thresholdguid in poweroutput.thresholdguids:
                poweroutput.thresholdguids.remove(thresholdguid)
                q.drp.meteringdevice.save(meteringdevice)
                break
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True