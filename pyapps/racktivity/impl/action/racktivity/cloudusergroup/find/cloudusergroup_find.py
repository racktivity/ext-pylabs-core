__author__ = 'racktivity'
__tags__ = 'cloudusergroup', 'find'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.cloudusergroup_find(name=params['name'],
                                                                              tags=params['tags'])}

def match(q, i, params, tags):
    return True

