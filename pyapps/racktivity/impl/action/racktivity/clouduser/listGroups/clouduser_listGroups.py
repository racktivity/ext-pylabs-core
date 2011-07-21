__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    clouduser = p.api.model.racktivity.clouduser.get(params['clouduserguid'])
    from rootobjectaction_lib import rootobjectaction_find
    groups = rootobjectaction_find.cloudusergroup_find()
    groupresult = []
    for group in groups:
        groupdetails = p.api.model.racktivity.cloudusergroup.get(group)
        if clouduser.guid in groupdetails.cloudusers:
            groupresult.append({"cloudusergroupguid": groupdetails.guid, "name": groupdetails.name, "description": groupdetails.description})
    result = []    
    result.append({"clouduserguid": clouduser.guid, "login": clouduser.login, "email": clouduser.email, "firstname":clouduser.firstname, "lastname": clouduser.lastname, "groups": groupresult})
    
    params['result'] = {'returncode': True,
                        'groupinfo': result}

def match(q, i, params, tags):
    return True
