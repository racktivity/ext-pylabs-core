__author__ = 'racktivity'
__priority__= 3

def main(q, i, p, params, tags):
    params['result'] = {'returncode':False}
    from rootobjectaction_lib import rootobjectaction_find
    jobs = rootobjectaction_find.job_find(clouduserguid=params['clouduserguid'])
    params['result'] = {'returncode': True,
                        'guidlist': jobs}

def match(q, i, params, tags):
    return True

