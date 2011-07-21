__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'getMonitoringInfo'
__priority__= 3

def getModule(client, deviceid):
    if deviceid.startswith("M"):
        raise RuntimeError("Module with id %s does not have monitorinfo")
    elif device.startswith("P"):
        return client.power
    elif device.startswith("T"):
        return client.temperature

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    datatype = params['datatype']
    module = getModule(rackclient, deviceid)
    params['result'] = module.getMonitor()


def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"

