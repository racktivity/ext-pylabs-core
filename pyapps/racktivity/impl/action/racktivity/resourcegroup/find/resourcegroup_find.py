__author__ = 'aserver'
__priority__= 3

from rootobjectaction_lib import rootobjectaction_find

def main(q, i, p, params, tags):
    params['result'] = {'returncode': True,
                        'guidlist': rootobjectaction_find.resourcegroup_find(name=params['name'],
                                             customerguid=params['customerguid'],
                                             description=params['description'],
                                             deviceguid=params['deviceguid'])} 
    
def match(q, i, params, tags):
    return True

