__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    cloudusergroup = p.api.model.racktivity.cloudusergroup.get(params['cloudusergroupguid'])
    result = []
    for group in cloudusergroup.cloudusergroups:
        groupdetails = p.api.model.racktivity.cloudusergroup.get(group)
        result.append({"cloudusergroupguid": groupdetails.guid, "name": groupdetails.name, "description": groupdetails.description})

    params['result'] = {'returncode': True,
                        'grouplist': result}

def match(q, i, params, tags):
    return True

