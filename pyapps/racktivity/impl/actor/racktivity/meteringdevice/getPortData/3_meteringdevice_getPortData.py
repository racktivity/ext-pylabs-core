__author__ = 'racktivity'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    datatype = params['datatype']
    portid = params['powerportid']
    methodname = "get%s" % datatype
    method = getattr(rackclient.power, methodname)
    errorcode, data = method(deviceid, int(portid))
    params['result'] = {'returncode': not bool(errorcode), 'value': data}


def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"

