__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'listUsers'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = q.drp.cloudusergroup.get(params['cloudusergroupguid'])
    result = []
    for user in cloudusergroup.cloudusers:
        clouduser = q.drp.clouduser.get(user)
        result.append({"clouduserguid": clouduser.guid, "name": clouduser.name, "login": clouduser.login, "email": clouduser.email, "firstname":clouduser.firstname, "lastname": clouduser.lastname})

    params['result'] = {'returncode': True,
                        'userlist': result}

def match(q, i, params, tags):
    return True

