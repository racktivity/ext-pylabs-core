__author__ = 'racktivity'
__tags__ = 'policy', 'list'
__priority__ = 3

def main(q,i,params,tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_list
    results = rootobjectaction_list.policy_list(policyguid=params['policyguid'],name=params['name'], \
                                                rootobjectaction=params['rootobjectaction'], rootobjecttype=params['rootobjecttype'])
    params['result'] = {'returncode':True, 'policyinfo':results}

def match(q,i,params,tags):
    return True
