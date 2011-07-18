__author__ = 'racktivity'
__tags__ = 'clouduser', 'find'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.clouduser_find(login=params['login'], email=params['email'], name=params['name'],
                                                                         status=params['status'], tags=params['tags'])}

def match(q, i, params, tags):
    return True
