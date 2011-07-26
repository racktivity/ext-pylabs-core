__author__ = 'racktivity'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    methodname = 'set' + params['configtype']
    configvalue = params['configvalue']
    kwargs = dict()
    kwargs['value'] = configvalue
    kwargs['moduleID'] = deviceid
    kwargs['portnumber'] = int(params['portnumber'])
    method = getattr(rackclient.power, methodname)
    errorcode = method(**kwargs)
    if errorcode:
        raise Exception("Setting port %s for '%s' failed, error code %d"%(params['thresholdtype'],params['deviceid'] , errorcode))
    params['result'] = True

def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"

