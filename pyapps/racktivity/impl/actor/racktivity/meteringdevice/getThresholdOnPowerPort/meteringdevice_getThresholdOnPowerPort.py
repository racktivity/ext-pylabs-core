__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getThresholdOnPowerPort'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    methodname = params['configtype']
    if methodname not in dir(rackclient.power):
        raise AttributeError('Power object has no attribute %s') % methodname
    kwargs['modeulID'] = deviceid
    kwargs['portnumber'] = int(params['portnumber'])
    method = getattr(rackclient.power, methodname)
    errorcode, data = method(**kwargs)
    params['result'] = {'returncode': not bool(errorcode), 'value': data}

def match(q, i, params, tags):
    return params['devicetype'] in "racktivity"

