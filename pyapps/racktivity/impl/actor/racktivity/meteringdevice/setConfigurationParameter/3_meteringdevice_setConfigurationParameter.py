__author__ = 'racktivity'

def getModule(client, moduleid):
    if moduleid.startswith("M"):
        return client.master, {}
    elif moduleid.startswith("P"):
        return client.power, {'moduleID': moduleid}
    elif moduleid.startswith("T"):
        return client.temperature, {'moduleID': moduleid}

def main(q, i, params, tags):
    rackclient = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    deviceid = params['deviceid']
    configtype = params['configtype']
    configvalue = params['configvalue']
    methodname = "set%s" % configtype
    module, kwargs = getModule(rackclient, deviceid)
    kwargs['value'] = configvalue
    method = getattr(module, methodname)
    errorcode = method(**kwargs)
    params['result'] = not bool(errorcode)


def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"

