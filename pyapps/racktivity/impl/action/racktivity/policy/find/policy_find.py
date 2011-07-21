__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode':True, 'guidlist': rootobjectaction_find.policy_find(name=params['name'], description=params['description'], \
                                                                                         rootobjecttype=params['rootobjecttype'], \
                                                                                         rootobjectaction=params['rootobjectaction'], \
                                                                                         rootobjectguid=params['rootobjectguid'], 
                                                                                         interval=params['interval'],
                                                                                         tags=params['tags'])}

def match(q, i, params, tags):
    return True
