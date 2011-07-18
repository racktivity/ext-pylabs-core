__author__ = 'racktivity'
__tags__ = 'errorcondition', 'find'
__priority__= 3

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    result = rootobjectaction_find.errorcondition_find(errorconditiontype=params['errorconditiontype'], timestamp=params['timestamp'], level=params['level'], \
                                                       agent=params['agent'], tags=params['tags'], application=params['application'])
    
    params['result'] = {'returncode': True,
                        'guidlist': result}

def match(q, i, params, tags):
    return True