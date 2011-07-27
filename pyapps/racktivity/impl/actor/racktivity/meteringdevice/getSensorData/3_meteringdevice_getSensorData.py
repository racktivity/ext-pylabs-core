__author__ = 'racktivity'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    datatype = params['datatype']
    methodname = "get%s" % datatype
    method = getattr(rackclient.temperature, methodname)
    errocode, data = method(deviceid)
    params['result'] = not bool(errorcode)
    params['value'] = data



def match(q, i, params, tags):
    return params['devicetype'] in "racktivity"

