__author__ = 'racktivity'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    datatype = params['datatype']
    datavalue = params['datavalue']
    portid = params['powerportid']
    
    methodname = "set%s" % datatype
    method = getattr(rackclient.power, methodname)
    errorcode = method(deviceid, datavalue,int(portid))
    
    params['result'] = {'returncode': not bool(errorcode)}


def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"

