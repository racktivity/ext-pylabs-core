__author__ = 'racktivity'
__tags__ = 'meteringdevice', 'setAccount'
__priority__= 3

def getModule(client, moduleid):
    if moduleid.startswith("M"):
        return client.master, {}
    elif moduleid.startswith("P"):
        return client.power, {'moduleID': moduleid}
    elif moduleid.startswith("T"):
        return client.temperature, {'moduleID': moduleid}

def main(q, i, params, tags):
    client = q.clients.racktivitycontroller.connect(params['deviceipaddress'], params['deviceapiport'], params['login'], params['password'])
    login = params['newlogin']
    password = params['newpassword']
    usertype = params['usertype']
    if usertype == "user":
        errorcode = client.master.setUserLoginAndPassword(login, password)
    elif usertype == "admin":
        errorcode = client.master.setAdminLoginAndPassword(login, password)
    elif usertype == "restricted":
        errorcode = client.master.setRestrictedLoginAndPassword(login, password)
    else:
        raise ValueError("Invalid type %s valid types are (user, admin and restricted)")
    params['result'] = (errorcode == 0)

def match(q, i, params, tags):
    return params['devicetype'] == "racktivity"
