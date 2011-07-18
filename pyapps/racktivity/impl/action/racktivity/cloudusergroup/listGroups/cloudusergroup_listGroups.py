__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'listGroups'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = q.drp.cloudusergroup.get(params['cloudusergroupguid'])
    result = []
    for group in cloudusergroup.cloudusergroups:
        groupdetails = q.drp.cloudusergroup.get(group)
        result.append({"cloudusergroupguid": groupdetails.guid, "name": groupdetails.name, "description": groupdetails.description})

    params['result'] = {'returncode': True,
                        'grouplist': result}

def match(q, i, params, tags):
    return True

