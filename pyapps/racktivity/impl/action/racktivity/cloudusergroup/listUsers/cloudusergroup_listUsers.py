__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = p.api.model.racktivity.cloudusergroup.get(params['cloudusergroupguid'])
    result = []
    for user in cloudusergroup.cloudusers:
        clouduser = p.api.model.racktivity.clouduser.get(user)
        result.append({"clouduserguid": clouduser.guid, "name": clouduser.name, "login": clouduser.login, "email": clouduser.email, "firstname":clouduser.firstname, "lastname": clouduser.lastname})

    params['result'] = {'returncode': True,
                        'userlist': result}

def match(q, i, params, tags):
    return True

