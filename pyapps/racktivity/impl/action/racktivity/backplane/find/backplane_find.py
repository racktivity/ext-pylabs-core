__author__ = 'racktivity'
__tags__ = 'backplane', 'find'

def main(q, i, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    params['result'] = {'returncode':True, 'guidlist': rootobjectaction_find.backplane_find(name=params['name'], managementflag=params['managementflag'], \
                                                                                            publicflag=params['publicflag'], storageflag=params['storageflag'], \
                                                                                            backplanetype=params['backplanetype'], tags=params['tags'])}

def match(q, i, params, tags):
    return True
