__author_ = 'racktivity'

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    portid = params['portid']
    status = rackclient.power.setPortState(moduleID=deviceid, value=0, portnumber=portid)
    if status == 0:
        params['result'] = True
    else:
        params['result'] = False

def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"
