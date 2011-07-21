__author__ = 'racktivity'

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    meteringdevice = p.api.model.racktivity.meteringdevice.get(params['meteringdeviceguid'])
    thresholdguid = params['thresholdguid']
    found = False
    for sensor in meteringdevice.sensors:
        if thresholdguid in sensor.thresholdguids:
            sensor.thresholdguids.remove(thresholdguid)
            p.api.model.racktivity.meteringdevice.save(meteringdevice)
            found = True
            break
    if not found:
        for poweroutput in meteringdevice.poweroutputs:
            if thresholdguid in poweroutput.thresholdguids:
                poweroutput.thresholdguids.remove(thresholdguid)
                p.api.model.racktivity.meteringdevice.save(meteringdevice)
                break
    params['result'] = {'returncode': True}

def match(q, i, params, tags):
    return True