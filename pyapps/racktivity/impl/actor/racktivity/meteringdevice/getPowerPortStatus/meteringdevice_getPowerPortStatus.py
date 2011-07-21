__author_ = 'racktivity'
__tags__ = 'meteringdevice', 'getPowerPortStatus'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    portid = params['portid']
    status, output = rackclient.power.getStatePortCur(moduleID=deviceid, portnumber=portid, length=1)
    
    params['result'] = {'returncode': not bool(status), 'status': output}

def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"
