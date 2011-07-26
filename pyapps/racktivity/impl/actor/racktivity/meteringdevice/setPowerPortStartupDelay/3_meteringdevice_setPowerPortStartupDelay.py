__author__ = 'racktivity'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    delay = params['delay']
    kwargs = dict()
    kwargs['value'] = delay
    kwargs['moduleID'] = deviceid
    kwargs['portnumber'] = int(params['portnumber'])
    errorcode = rackclient.power.setDelayOn(**kwargs)
    if errorcode:
        raise Exception("Setting port startup delay for '%s' failed, error code %d"%(params['deviceid'], errorcode))
    params['result'] = True 

def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"
