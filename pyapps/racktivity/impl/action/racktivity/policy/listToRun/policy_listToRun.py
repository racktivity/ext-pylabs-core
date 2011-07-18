__author__ = 'racktivity'
__tags__ = 'policy', 'listToRun'
__priority__ = 3

import time

def main(q,i,params,tags):
    params['result'] = {'returncode':False}
    now = int(time.time())
    
    results = q.drp.policy.query("""SELECT guid, description, interval, lastrun, maxduration, maxruns, name, policyparams,
                          rootobjectaction, rootobjectguid, rootobjecttype, runbetween, runnotbetween, status, tags
                          FROM policy.view_policy_list
                          WHERE cast("lastrun" as numeric) + (to_number("interval", '99999999.99') * 60.0) <= %d or lastrun is null;""" % now)
    
    params['result'] = {'returncode':True, 'policyinfo': results}

def match(q,i,params,tags):
    return True
